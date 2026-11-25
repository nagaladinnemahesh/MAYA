from tools.system_tools import SystemTools


class CommandProcessor:

    def __init__(self):
        self.system = SystemTools()

    def process(self, command):

        command = command.lower().strip()

        if "open notepad" in command:
            return self.system.open_notepad()

        elif "open calculator" in command:
            return self.system.open_calculator()

        elif "open youtube" in command:
            return self.system.open_youtube()

        elif "time" in command:
            return self.system.get_time()

        elif "date" in command:
            return self.system.get_date()

        else:
            return "I'm sorry sir. I don't understand that command yet."