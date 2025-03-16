from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine-tuning.
build_options = {"packages": ["os", "kivy", "selenium", "google_generativeai"], "excludes": []}

# GUI applications require a different base on Windows
base = None

# Define the executable
executables = [Executable("main.py", base=base, target_name="NceaBot.exe")]

# Setup cx_Freeze
setup(
    name="NceaBot",
    version="0.1",
    description="NCEA Bot Application",
    options={"build_exe": build_options},
    executables=executables
)
