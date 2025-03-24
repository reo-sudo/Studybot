import google.generativeai as ai
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDIconButton
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
from selenium.common.exceptions import WebDriverException
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
    

    MDBoxLayout:
        orientation: "vertical"
        padding: "16dp"
        spacing: "16dp"

        MDLabel:
            id: mainNCA
            text: "Study Bot"
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
                password: True
            

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


    MDIconButton:
        text: "Switch Theme"
        icon: "theme-light-dark"
        pos_hint: {"right": 1 }
        on_release: app.change_theme()

    

    
"""


class NceaBot(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_style = "Blue"
        return Builder.load_string(KV)
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = None
        self.api_key = None
        self.model = None
        self.dialog = None


    def change_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
            self.root.ids.mainNCA.text_color = (0,0, 0, )
            self.update_status("Theme Changed to Light")
        else:
            self.theme_cls.theme_style = "Dark"  
            self.root.ids.mainNCA.text_color = (1, 1, 1, 1)
            self.update_status("Theme Changed to Dark")
            
        
 
   
        
    def save_api_key(self):
        new_key = self.root.ids.api_input.text.strip()
        if new_key:
            self.api_key = new_key
            ai.configure(api_key=self.api_key)
            self.model = ai.GenerativeModel("gemini-2.0-flash")
            self.update_status("API key Saved")
        else:
           self.show_dialog("No API ERROR", "There is no API key")
           self.update_status("No API Input")

    def chrome_click(self):
        if not self.api_key:
            self.show_dialog("No API ERROR", "There is no api key")
            self.update_status("NO api input")
            return
        
        try:
            ai.configure(api_key=self.api_key)
            self.model.generate_content("Test API key")
            self.update_status("API key verified. Launching Brower...")
        except Exception as e:
            self.show_dialog("Invalid API Key", "Your api key is not Valid")
            self.update_status("Invalid API Key")
            return
        
       

        
        try:
            if self.driver is None or not self.is_driver_valid():
                options = webdriver.ChromeOptions()
                options.add_experimental_option("detach", True)
                self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                self.driver.get("http://taku.nzqa.govt.nz/login-landing-page/")
                self.show_dialog("Login Required", "Enter your Login info")
                self.update_status("Browser Launched")
            else:
                try:
                    self.driver.get("http://taku.nzqa.govt.nz/login-landing-page/")
                    self.update_status("Browser already Launched")
                except WebDriverException as e:
                    if "session not created" in str(e) or "no such session" in str(e):
                        self.driver.quit()
                        self.driver = None
                        self.chrome_click()
                        return
                else:
                    raise e
        except Exception as e:
            self.show_dialog("Browser Error", f"Browser Error {e}")
            self.update_status("Error Launching Browser")

    def is_driver_valid(self):
        try:
            self.driver.title
            return True
        except WebDriverException:
            self.update_status("Browser Closed")
            return False



    def fetch_results(self,):
      
       if not self.driver:
           self.show_dialog("Browser Error", "Brower has not Lauched. Please lanch the Browser First.")
           return
           

       try:
            
            
            current_url = self.driver.current_url 
            if "secure.nzqa.govt.nz/for-learners/records/my-entries-results" in current_url:
                    self.update_status("Fetching Results...")
                    text_content = self.driver.page_source
                    if text_content:
                        with open('text_content.txt', 'w', encoding="utf-8") as file:
                            file.write(text_content)
                        self.update_status("Results Saved")
                    else:
                        self.show_dialog("No Results Error","Nothing is here" )
                        self.update_status("Error Nothing found")
            else:
                self.show_dialog("Wrong URL", "Please go to the Right page")
                self.update_status("not on results page")
       except Exception as e:
           self.show_dialog(" Fetch Error", f"Failed to fecth results: {str(e)}")
           self.update_status("Error Fetching Results")
        

              
    def save_prompt(self):
        try:
        
            with open('text_content.txt', 'r', encoding="utf-8") as file:
                text_content = file.read()
        except FileNotFoundError:
            self.show_dialog("file Error", "no text_content.txt found")
            return
        
        new_prompt = self.root.ids.prompt_input.text.strip()
        if not new_prompt:
            self.show_dialog("No Prompt Error", "There is no Prompt")
            self.update_status("No prompt input")
            return
        
        prompt = f"{new_prompt}\n\nAnalyze the following Ncea Results page content:\n{text_content} "
        
        try: 
                response = self.model.generate_content(prompt).text
        except Exception as c:
               if "API key not valid" in str(c):
                   self.show_dialog("API key Error", "API key is missing or invalid")
               else:
                   self.show_dialog("API Error", f"something went wrong: {c}")
                   return
        
        print("new Prompt saved")
        self.show_dialog(f"prompt Saved", new_prompt)
        self.update_status(f"prompt updated")

        try:
               with open('response.txt', 'w', encoding="utf-8") as file:
                file.write(response)
                print("results have been saved successesfully")
                self.update_status("Prompt Saved")
        except Exception as a:
               self.show_dialog("File Error", f"Could not save results: {a}")

       

    def show_popup(self):
        try:

            with open('response.txt', 'r', encoding="utf-8") as file:
                Response_text = file.read()
        except FileNotFoundError:
            self.show_dialog("File not found error", "No file is there")
            return
        
        
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

    def update_status(self, status_text):
        self.root.ids.status_label.text = f"Status: {status_text}"
       

if __name__ == "__main__":
    NceaBot().run()
