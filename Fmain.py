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

KV = """
MDScreen:
    md_bg_colors: 0.1, 0.1, 0.1, 1

    MDLabel:
        text: "Ncea ask"
        font_style: "H4"
        halign: "center"
        pos_hint: {"center_y": 0.9}
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1

    MDTextField:
        id: api_input
        hint_text: "Enter an API Key"
        model: "rectangle"
        size_hint_x: 0.8
        pos_hint: {"center_x":0.5, "y": 0.75}

    MDRaisedButton:
        text: "Save api key"
        pos_hint: {"center_x": 0.5, "y": 0.65}    
        on_release: app.save_api_key()
        md_bg_color: 0.2, 0.6,  1, 1

    MDTextField:
        id: prompt_input
        hint_text: "Enter Prompt"
        model: "rectangle"
        size_hint_x: 0.8
        pos_hint: {"center_x": 0.5, "y": 0.55}


    MDRaisedButton:
        text: "Save Prompt"
        pos_hint: {"center_x": 0.5, "y": 0.45}
        on_release: app.save_prompt()
        md_bg_color: 1, 0.4, 0.2, 1

    MDRaisedButton:
        text: "Start"
        pos_hint: {"center_x": 0.5, "y": 0.35}
        on_release: app.chrome_click()
        md_bg_color: 0.2, 0.6, 1, 1

    MDRaisedButton:
        text: "fetch Results"
        pos_hint: {"center_x": 0.5, "y": 0.25}
        on_release: app.fetch_results()
        md_bg_color: 1, 0.4, 0.2, 1

    MDRaisedButton:
        text: "show Results"
        pos_hint: {"center_x": 0.5, "y": 0.15}
        on_release: app.show_popup()
        md_bg_color: 0.2, 0.6, 1, 1

"""

if platform.system() == 'Windows':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


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
         driver = webdriver.Chrome()
         options = webdriver.ChromeOptions()
         options.add_experimental_option("detach", True)
         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get("https://login.nzqa.govt.nz/")
        self.show_dialog("Login Required", "Enter your Login info")
        

    def fetch_results(self,):
       global driver
       if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":
        text_content = driver.page_source
        if not text_content:
                self.show_dialog("No text_content", "There is no text_content")
                return
        else:
            if driver.current_url == None:
                self.show_dialog("Fetch Error", "There is nothing here")
                return
                    
        

        
        prompt = f"prompt :\n{text_content} "

        response = model.generate_content(prompt).text
       
    def save_prompt(self):
        global prompt
        new_prompt = self.root.ids.prompt_input.text.strip()
        if new_prompt:
           prompt = new_prompt
           response = model.generate_content(prompt).text
           print("new Prompt saved")
           with open('response.txt', 'w', encoding="utf-8") as file:
                file.write(response)
                print("results have been saved successesfully")
        else:
            self.show_dialog("No Prompt ERROR", "There is no Prompt" )

    def show_popup(self, Response_text):
        
        content = MDScrollView()
        label = MDLabel(
            text=Response_text,
            theme_text_color="Primary",
            halign="center",
            size_hint_y=None,
            height=200
        )
        content.add_widget(label)

        dialog = MDDialog(
            title="Results From AI",
            type="custom",
            content_cls=content,
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
