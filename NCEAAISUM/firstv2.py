import tkinter as tk
from tkinter import *
from tkinter import messagebox
import google.generativeai as ai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

API_KEY = 'add API key here'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-2.0-flash")

root = Tk()
root.geometry('225x150')
root.title("Ncea bot")
root.resizable(False, False)


icon_image = PhotoImage(file="/Users/ruderakshmoudgill/NCEAAISUM/NCEQ ICON.png")

root.iconphoto(True, icon_image)

background_image = PhotoImage(file="/Users/ruderakshmoudgill/NCEAAISUM/Ncea_background.png")

background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

driver = None


def start_broswer():
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://login.nzqa.govt.nz")
        messagebox.showinfo("Login required","enter your log in info to proceed")
    else:
        messagebox.showinfo("info", "broswer is already running")

def get_data():
    global driver
    
    if driver is None:
        messagebox.showinfo("info", "you must start your browser first!")
        return
    
    
       

    if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":
        text_content = driver.page_source
        if not text_content:
            messagebox.showerror("error", "Error: no text found")
    else:
        messagebox.showerror("Error", "Not the correct Page Please go to 'My Entries & Results'.")
        return   
    

    prompt = f"Summarize the following in the file and show my results but like only my credits also number of credits over the years and other things keep it short but say it nice and normal perosn and human like way also tell how i can improve as well :\n{text_content} "

    response = model.generate_content(prompt)

    with open('response.txt', 'w', encoding="utf-8") as file:
        file.write(response.text)

    with open('response.txt', 'r', encoding="utf-8") as file:
        Resp = file.read()

    messagebox.askokcancel("Results", Resp)


    os.system(f'say -f response.txt ')




b = Button(root, text="Open NZQA LOGIN", command=start_broswer, width=20, height=2)
b.pack(pady=10) 

b2 = tk.Button(root, text="Show Results", command=get_data, width=20, height=2, )
b2.pack(pady=10)
    
root.mainloop()


