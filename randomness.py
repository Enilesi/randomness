import os
from dotenv import load_dotenv
load_dotenv() 


from time import sleep
import random
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import psycopg2

try:
    connection = psycopg2.connect(
        dbname="randomness",
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST")
    )

    cursor = connection.cursor()
    
except Exception as e:
    print(f"An error occurred: {e}")

chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")


with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options) as driver:
    
    driver.get("https://randomtextgenerator.com/")
    for i in range(1000):
        language_dropdown = Select(driver.find_element(By.NAME, "language"))
        options = language_dropdown.options
        if options:
            random_option = random.choice(options)
            language = random_option.text
            language_dropdown.select_by_visible_text(language)
            print(f"Randomly selected option: {language}")
            button = driver.find_element(By.NAME,"Go")
            button.click()
            print(f"Button clicked {i+1} time(s)")
            sleep(2)
            generated_text_box = driver.find_element(By.ID, "randomtext_box")
            now = datetime.datetime.now()
            with connection.cursor() as cursor:
                cursor.execute(
                    """ insert into generated_text(language,text,date_time)  values (%s,%s,%s)""",
                    (language,generated_text_box.text,now),
                )
                connection.commit()
        else:
            print("No options available in the dropdown")



