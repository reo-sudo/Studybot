from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


driver = None

class NceaBot(App):
    def build(self):
        layout = FloatLayout()
        Label1 = Label(text="Ncea Bot")
        layout = BoxLayout(orientation='vertical')
        btn1 = Button(
           text="start",
           size_hint=(None, None),
           size=(200,100 ),
           pos_hint = {'x':.100,'y':.200}
        )
        
        btn1.bind(on_press=self.chrome_click)

    
        layout.add_widget(btn1)
        layout.add_widget(Label1)

        return layout
    
    def chrome_click(self, instance):
     global driver
     if driver is None:
         options = webdriver.ChromeOptions()
         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
         driver.get("https://www.google.com/")


if __name__ == "__main__":
    NceaBot().run()


