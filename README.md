NCEA Helper Bot
A smart assistant that helps students track their NCEA progress by analyzing their results and providing feedback.

How It Works:
The bot scans the official NCEA website, retrieves the student's current NCEA level and progress, and generates a personalized progress report.
It uses Selenium for web automation and an open-source AI model (e.g., Google Generative AI) to process the data and provide insights.

How It Runs:
Selenium launches Chrome, allowing the user to log in.
After logging in and navigating to the results page, the user presses Enter in the terminal.
The bot fetches the results, generates a structured feedback file, and displays key insights in the terminal.
The feedback file uses os.system(f'say "{results}"') to optionally read out the results aloud.

Tech Stack:
Selenium (for browser automation)
Google Generative AI (or any free AI model)
Python (os module) for system operations




![image](https://github.com/user-attachments/assets/5d911ef7-ce0b-4a1f-84d6-181fce356dae)
