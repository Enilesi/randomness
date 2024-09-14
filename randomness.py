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





class DataCollector:
    def __init__(self) -> None:
        self.init_db()
        self.init_chrome_options()
    def init_db(self):
        self.connection = psycopg2.connect(
            dbname="randomness",
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            host=os.getenv("HOST")
        )

    def init_chrome_options(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-search-engine-choice-screen")
    
    def start(self):
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=self.chrome_options) as driver:
            driver.get("https://randomtextgenerator.com/")
            while True:
                self.collect_data(driver)

    def collect_data(self,driver):
        language_dropdown = Select(driver.find_element(By.NAME, "language"))
        options = language_dropdown.options

        if not options:
            raise Exception("No options available in the dropdown")
        
        random_option = random.choice(options)
        language = random_option.text
        language_dropdown.select_by_visible_text(language)
    
        button = driver.find_element(By.NAME,"Go")
        button.click()
        sleep(2)

        generated_text_box = driver.find_element(By.ID, "randomtext_box")
        self.insert_into_db(language,generated_text_box.text)


    def insert_into_db(self,language,text):
         with self.connection.cursor() as cursor:
                cursor.execute(
                    """ insert into generated_text(language,text,date_time)  values (%s,%s,%s)""",
                    (language,text,datetime.datetime.now()),
                )
                self.connection.commit()



def main():
    colleror=DataCollector()
    colleror.start()

if __name__ == "__main__":
    main()