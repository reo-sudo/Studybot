 # Study Bot App 🚀


 ## NCEA Helper Bot
A machine that analyzes results and gives students feedback on their progress through NCEA.

 ## How Does This Work: 
The bot scrapes the official NCEA site, obtains the student’s current NCEA level and progress and provide a personalized progress report. In it, Selenium is used to automate the web, and an open-source AI model (like Google Generative AI) that scrapes the data and generates insights.

## How It Runs:
Selenium opens up Chrome to let the user log in. The user logs in and from the results page, presses Enter in the terminal. The bot retrieves the results, creates a structured feedback file, and then shows important findings in the command line. The feedback file uses os. Add system(f'say "{results}"') to read the results out loud if you want.

First Segment: Selenium (To automate a Chrome browser) Google Generative AI (free AI model) Python (os module)

## My Documentation:
https://docs.google.com/presentation/d/1V3y1-wqX5NeL1nJGCLA2tKD78fpprTJNimVA7j_nZpY/edit?usp=sharing


![image](https://github.com/user-attachments/assets/5d911ef7-ce0b-4a1f-84d6-181fce356dae)

## App link for diffrent os:
1.Mac link: 
https://github.com/reo-sudo/Studybot/releases/tag/NceaBotMac

2.Windows link: 
https://github.com/reo-sudo/Studybot/releases/tag/NceaBotWindows

## How to Use:

![image](https://github.com/user-attachments/assets/f64d1aee-38a2-482f-8736-0d61df33d0be)

---------------------------------------------------------------------------
# Running the App by code 💻
If the user wants to run the add by the code instead of using the app

## follow these steps:
Have the latest version of Python Installed 3.7+
# clone the Repo
git clone https://github.com/your-username/Studybot.git
cd Studybot
# install Dependencies:
pip install -r requirements.txt
# Run the App
python run_NCEAAISUM/nceapro3.1.py





