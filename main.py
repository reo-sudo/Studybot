import google.generativeai as ai
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.lang import builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from kivy.graphics import Color, Rectangle
import os
import platform

if platform.system() == 'Windows':
    os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'


API_KEY = 'enter api'
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-2.0-flash")

driver = None

class NceaBot(App):
    def build(self):
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.1,0.5,0.8,1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self.update_rect, pos=self.update_rect)
            
        Label1 = Label(text="[b]To start enter API key[/b]",
                       markup=True,
                       font_size=30,
                       color=(1,1,1,1),
                       pos_hint={'center_x': 0.5, 'top': 0.95}
        )
        
            
        btn1 = Button(
           text="start",
           size_hint=(0.4, 0.1),
           pos_hint = {'center_x': 0.5, 'y': 0.7},
           background_color=('white')
           
           
        )
       
        btn2 = Button(
           text="fetch results",
           size_hint=(0.4, 0.1),
           pos_hint = {'center_x': 0.5, 'y': 0.6},
    )

        

        self.api_display = TextInput(
            text=f"API KEY: {API_KEY[:10]}....", readonly=True,
            size_hint=(0.8, 0.05),
            pos_hint={'center_x': 0.5, 'y': 0.35},

        )

        
        self.api_input = TextInput(
            hint_text="Enter new API key",
            size_hint=(0.8, 0.05),
            pos_hint={'center_x': 0.5, 'y': 0.25},

        )
        
        s_b = Button(
            text="save api key",
            size_hint=(0.4, 0.07),
            pos_hint={'center_x': 0.5, 'y': 0.16}
        )
        
        
        m_b = Button(text="show results", 
                     size_hint=(0.3, 0.05),
                     pos_hint={'center_x': 0.5, 'y': 0.5})
        

        self.prompt_input = TextInput(
           hint_text="Enter new Prompt",
           size_hint=(0.8, 0.05),
           pos_hint={'center_x': 0.5, 'y': 0.1}
        )

        p_b = Button(text="save prompt",
                     size_hint=(0.3,  0.1),
                     pos_hint={'center_x': 0.5, 'y': 0.%1})

        
        btn1.bind(on_press=self.chrome_click)
        btn2.bind(on_press=self.fetch_results)
        s_b.bind(on_press=self.save_api_key)
        m_b.bind(on_press=self.show_popup)
        p_b.bind(on_press=self.save_prompt)
       
        layout.add_widget(Label1)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(self.api_input)
        layout.add_widget(self.api_display)
        layout.add_widget(s_b)
        layout.add_widget(m_b)
        layout.add_widget(self.prompt_input)
        layout.add_widget(p_b)
        
        return layout
    
    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        
    def save_api_key(self, instance):
        global API_KEY
        new_key = self.api_input.text.strip()
        if new_key:
            API_KEY = new_key
            ai.configure(api_key=API_KEY)
            self.api_display.text = f"API KEY: {API_KEY[:10]}..."
            print(f"API key Updated: {API_KEY}")

    def chrome_click(self, instance):
     global driver
     if driver is None:
         options = webdriver.ChromeOptions()
         options.add_experimental_option("detach", True)
         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
         driver.get("https://login.nzqa.govt.nz/")

    def fetch_results(self, instance):
       global driver
       if driver.current_url == "https://secure.nzqa.govt.nz/for-learners/records/my-entries-results.do":
        text_content = driver.page_source
        if not text_content:
                return

        
        prompt = f"prompt :\n{text_content} "

        response = model.generate_content(prompt).text
       
    def save_prompt(self, intance):
        global prompt
        new_prompt = self.prompt_input.text.strip()
        if new_prompt:
           prompt = new_prompt
           response = model.generate_content(prompt).text
           print("new Prompt saved")


        with open('response.txt', 'w', encoding="utf-8") as file:
            file.write(response)
        print("results have been saved successesfully")

    def show_popup(self, insatance):
       if not  os.path.exists('response.txt'):
        print("No Results found")
        return
       
       with open('response.txt', 'r', encoding="utf-8") as file:
        response_text = file.read()

        scroll_view = ScrollView(size_hint=(1, 1))
        label = Label(
                text=response_text,
                text_size=(600, None),
                size_hint=(1, None),
                height=200,
                font_size=15,
                size_hint_y=None)
        
        
            
        scroll_view.add_widget(label)
        popup = Popup(title="Ncea Results",
                  content=scroll_view,
                  size_hint=(None, None),
                  size=(700, 600))


        
            
            
        popup.open()


if __name__ == "__main__":
    NceaBot().run()
