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
        btn1.bind(on_press=self.chrome_click)

        btn2 = Button(
           text="fetch results",
           size_hint=(0.4, 0.1),
           pos_hint = {'center_x': 0.5, 'y': 0.6},
    )

        btn2.bind(on_press=self.fetch_results)

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
            pos_hint={'center_x': 0.5, 'y': 0.15}
        )
        
        s_b.bind(on_press=self.save_api_key)

        m_b = Button(text="show results", 
                     size_hint=(0.3, 0.05),
                     pos_hint={'center_x': 0.5, 'y': 0.5})

        m_b.bind(on_press=self.show_popup)
       
        layout.add_widget(Label1)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(self.api_input)
        layout.add_widget(self.api_display)
        layout.add_widget(s_b)
        layout.add_widget(m_b)
        
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

        
        prompt = f"""
        Summarize the following in the file and show my results but like only my credits also number of credits over the years and other things keep it short  like 50 
        words but say it nice and normal perosn and human like way also tell how i can improve as well :\n{text_content} 
        """

        response = model.generate_content(prompt).text
       

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

