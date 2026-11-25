import subprocess
import webbrowser
from datetime import datetime


class SystemTools:

    def open_notepad(self):
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad, sir."

    def open_calculator(self):
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator, sir."

    def open_youtube(self):
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube, sir."

    def get_time(self):
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Sir, the current time is {current_time}."

    def get_date(self):
        current_date = datetime.now().strftime(
            "%A, %d %B %Y"
        )
        return f"Today is {current_date}, sir."