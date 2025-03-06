import google.generativeai as ai
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
import os

API_KEY = 'AIzaSyDLx7w5pESiTMfBnlzawQxwc_e7S8ARW2Y'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-2.0-flash")


options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://login.nzqa.govt.nz")

input("log in manually, then press enter here...")

if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":
    html = driver.page_source
with open (html , 'r', encoding="utf-8")as file:
  text_content =  file.read(html)


input("start ai : ")

prompt = f"Summarize the following in the file and show my results but like only my credits over the years and other things keep it short but say it nice and normal perosn and human like way {text_content} "

response = model.generate_content(prompt)

with open('response.txt', 'w', encoding="utf-8") as file:
    file.write(response.text)

with open('response.txt', 'r', encoding="utf-8") as file:
    Resp = file.read()
    os.system(f'say "{Resp}"')

driver.quit()

