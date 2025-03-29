1| import google.generativeai as ai  # Importing the Google Generative AI library
2| from selenium import webdriver  # Importing Selenium WebDriver for browser automation
3| from selenium.webdriver.support.ui import WebDriverWait  # Importing WebDriverWait for explicit waits
4| from selenium.webdriver.support import expected_conditions as EC  # Importing expected_conditions for waiting
5| from selenium.webdriver.chrome.service import Service  # Importing Service for ChromeDriver management
6| from webdriver_manager.chrome import ChromeDriverManager  # Importing ChromeDriverManager to auto-install ChromeDriver
7| from selenium.webdriver.common.by import By  # Importing By for element location strategies
8| import undetected_chromedriver as uc  # Importing undetected_chromedriver to avoid detection of automation
9| import time  # Importing time for sleep functionality
10| import os  # Importing os for operating system interactions
11| 
12| API_KEY = 'add API key here'  # Placeholder for the API key
13| ai.configure(api_key=API_KEY)  # Configuring the AI with the provided API key
14| model = ai.GenerativeModel("gemini-2.0-flash")  # Initializing the generative model
15| 
16| 
17| options = webdriver.ChromeOptions()  # Setting up Chrome options
18| options.add_experimental_option("detach", True)  # Option to keep the browser open after the script finishes
19| 
20| driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # Initializing ChromeDriver
21| 
22| driver.get("https://login.nzqa.govt.nz")  # Navigating to the NZQA login page
23| 
24| input("log in manually, then press enter here...")  # Prompting user to log in manually
25| 
26| if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":  # Checking if logged in successfully
27|     html = driver.page_source  # Getting the page source
28| with open (html , 'r', encoding="utf-8")as file:  # Opening the HTML file
29|   text_content =  file.read(html)  # Reading the HTML content
30| 
31| 
32| input("start ai : ")  # Prompting user to start the AI
33| 
34| prompt = f"Summarize the following in the file and show my results but like only my credits over the years and other things keep it short but say it nice and normal person and human-like way {text_content}"  # Creating a prompt for the AI
35| 
36| response = model.generate_content(prompt)  # Generating content using the AI model
37| 
38| with open('response.txt', 'w', encoding="utf-8") as file:  # Writing the AI response to a file
39|     file.write(response.text)
40| 
41| with open('response.txt', 'r', encoding="utf-8") as file:  # Reading the AI response from the file
42|     Resp = file.read()
43|     os.system(f'say "{Resp}"')  # Using the os.system command to read out the response
44| 
45| driver.quit()  # Quitting the browser
46| 
47| 
