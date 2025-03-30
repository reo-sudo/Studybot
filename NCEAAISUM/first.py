1| import google.generativeai as ai 
2| from selenium import webdriver 
3| from selenium.webdriver.support.ui import WebDriverWait  
4| from selenium.webdriver.support import expected_conditions as EC 
5| from selenium.webdriver.chrome.service import Service  
6| from webdriver_manager.chrome import ChromeDriverManager  
7| from selenium.webdriver.common.by import By 
8| import undetected_chromedriver as uc  
9| import time  
10| import os 
11| 
12| API_KEY = 'add API key here'  
13| ai.configure(api_key=API_KEY)  
14| model = ai.GenerativeModel("gemini-2.0-flash")  
15| 
16| 
17| options = webdriver.ChromeOptions()  
18| options.add_experimental_option("detach", True)  
19| 
20| driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  
21| 
22| driver.get("https://login.nzqa.govt.nz")  
23| 
24| input("log in manually, then press enter here...")  
25| 
26| if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":  
27|     html = driver.page_source  
28| with open (html , 'r', encoding="utf-8")as file:  
29|   text_content =  file.read(html) 
30| 
31| 
32| input("start ai : ")  
33| 
34| prompt = f"Summarize the following in the file and show my results but like only my credits over the years and other things keep it short but say it nice and normal person and human-like way {text_content}"  # Creating a prompt for the AI
35| 
36| response = model.generate_content(prompt)  
37| 
38| with open('response.txt', 'w', encoding="utf-8") as file: 
39|     file.write(response.text)
40| 
41| with open('response.txt', 'r', encoding="utf-8") as file:  
42|     Resp = file.read()
43|     os.system(f'say "{Resp}"')  
44| 
45| driver.quit() 
46| 
47| 
