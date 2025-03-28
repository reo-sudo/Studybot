import google.generativeai as ai
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivymd.uix.scrollview import MDScrollView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
import os
import platform

if platform.system() == 'Windows':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

KV = """
MDScreen:
    md_bg_color: 0.1, 0.1, 0.1, 1

    MDBoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "16dp"

        MDLabel:
            text: "Ncea Bot"
            font_style: "H4"
            halign: "center"
            size_hint_y: None
            height: "64dp" 
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1

        MDSeparator:
            height: "1dp"

        MDBoxLayout:
            orientation: "vertical"
            spacing: "8dp"
            size_hint_y: None
            height: "100dp"

            MDLabel:
                text: "API Configuration"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 0.2, 0.6, 1, 1
                size_hint_y: None
                height: "32dp"

 
            MDTextField:
                id: api_input
                hint_text: "Enter an API Key"
                helper_text: "Required to Process NCEA Results"
                mode: "rectangle"
                size_hint_x: 1
                size_hint_y: None
                height: "480dp"
            

            MDRaisedButton:
                text: "Save API key"
                pos_hint: {"right": 1}    
                on_release: app.save_api_key()
                md_bg_color: 0.2, 0.6,  1, 1
                size_hint_y: None
                height: "48dp"

        MDSeparator:
            height: "1dp"

        MDBoxLayout:
            orientation: "vertical"
            spacing: "8dp"
            size_hint_y: None
            height: "140dp"

            MDLabel:
                text: "Prompt Configuration"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color:  1, 0.4, 0.2, 1
                size_hint_y: None
                height: "32dp"

            MDTextField:
                id: prompt_input
                hint_text: "Enter Prompt"
                helper_text: "Required to get info on your work"
                helper_text_mode: "on_focus"
                mode: "rectangle"
                multiline: True
                size_hint_x: 1
                size_hint_y: None
                height: "80dp"

            MDRaisedButton:
                text: "Save Prompt"
                pos_hint: {"right": 1}
                on_release: app.save_prompt()
                md_bg_color: 1, 0.4, 0.2, 1
                size_hint_y: None
                height: "48dp"

        MDSeparator:
            height: "1dp"

    
        MDBoxLayout:
            orientation: "vertical"
            spacing: "8dp"
            

            MDLabel:
                text: "Browser Actions"
                font_style: "H6"
                theme_text_color: "Custom"
                text_color: 0.2, 0.8, 0.2, 1
                size_hint_y: None
                height: "32dp"

            MDGridLayout:
                cols: 2
                spacing: "8dp"
                size_hint_y: None
                height: "48dp"

                MDRaisedButton:
                    text: "Launch Browser"
                    size_hint_x: 0.5
                    on_release: app.chrome_click()
                    md_bg_color: 0.2, 0.6, 1, 1
                    size_hint_y: None
                    height: "48dp"

                MDRaisedButton:
                    text: "fetch Results"
                    size_hint_x: 0.5
                    on_release: app.fetch_results()
                    md_bg_color: 1, 0.4, 0.2, 1
                    size_hint_y: None
                    height: "48dp"

            MDRaisedButton:
                text: "show Results"
                size_hint_x: 1
                on_release: app.show_popup()
                md_bg_color: 0.2, 0.8, 0.2, 1
                size_hint_y: None
                height: "48dp"
        
        MDLabel:
            id: status_label
            text: "Status: Ready"
            font_style: "Caption"
            theme_text_color: "Secondary"
            size_hint_y: None
            height: "24dp"

    
"""

API_KEY = 'enter api'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-2.0-flash")

driver = None

class NceaBot(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_style = "Blue"
        return Builder.load_string(KV)

        
        
 
   
        
    def save_api_key(self):
        global API_KEY
        new_key = self.root.ids.api_input.text.strip()
        if new_key:
            API_KEY = new_key
            ai.configure(api_key=API_KEY)
            print(f"API key Updated: {API_KEY}")
        else:
           self.show_dialog("No API ERROR", "There is no API key")

    def chrome_click(self):
        global driver
        if driver is None:
         options = webdriver.ChromeOptions()
         options.add_experimental_option("detach", True)
         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("http://taku.nzqa.govt.nz/login-landing-page/")
        self.show_dialog("Login Required", "Enter your Login info")
        

    def fetch_results(self,):
       global driver
       if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":
        text_content = driver.page_source
        if text_content:
            with open('text_content.txt', 'w', encoding="utf-8") as file:
                file.write(text_content)
                print("Reuslts saved from page")
        else:
             self.show_dialog("No text_content", "There is no text_content")
       else:
           self.show_dialog("No Results here", "No content Found")
               
        
        
       


    def save_prompt(self):
        try:
        
            with open('text_content.txt', 'r', encoding="utf-8") as file:
                text_content = file.read()
        except FileNotFoundError:
            self.show_dialog("file Error", "no text_content.txt found")
            return
        
        new_prompt = self.root.ids.prompt_input.text.strip()
        if new_prompt:
           prompt = f"{new_prompt}\n{text_content}"
           response = model.generate_content(prompt).text
           print("new Prompt saved")
           self.show_dialog(f"prompt Saved", new_prompt)
           with open('response.txt', 'w', encoding="utf-8") as file:
                file.write(response)
                print("results have been saved successesfully")
        else:
            self.show_dialog("No Prompt ERROR", "There is no Prompt" )

    def show_popup(self):

        with open('response.txt', 'r', encoding="utf-8") as file:
            Response_text = file.read()
        
        
            dialog = MDDialog(
            title="Results From AI",
            text=Response_text,
            size_hint=(0.9, 0.8),
            buttons=[
                MDRaisedButton(
                    text="Close",
                    md_bg_color=(1, 0.4, 0.2, 1),
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def show_dialog(self, title, text):
        dialog = MDDialog(title=title, text=text, size=(0.8 ,0.4))
        dialog.open()

       

if __name__ == "__main__":
    NceaBot().run()
