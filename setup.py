from cx_Freeze import setup, Executable

# List all the imports to be explicitly included in the build
includes = [
    'google.generativeai',
    'selenium',
    'kivy.app',
    'kivy.uix.label',
    'kivy.uix.button',
    'kivy.uix.boxlayout',
    'kivy.uix.textinput',
    'kivy.uix.gridlayout',
    'kivy.uix.floatlayout',
    'kivy.uix.popup',
    'kivy.uix.widget',
    'kivy.lang',
    'kivy.uix.screenmanager',
    'kivy.uix.scatter',
    'kivy.uix.scrollview',
    'webdriver_manager.chrome',
    'selenium.webdriver.chrome.service',
    'os',
]

# Define the setup configuration
setup(
    name="NceaBot",
    version="1.0",
    description="NceaBot app",
    options={
        'build_exe': {
            'packages': ['os', 'kivy', 'selenium', 'webdriver_manager'],
            'includes': includes,  # Include all necessary imports
        }
    },
    executables=[Executable("main.py")],
)
