from tools.system_tools import SystemTools
from tools.system_monitor import SystemMonitor


class CommandProcessor:

    def __init__(self):
        self.system = SystemTools()
        self.monitor = SystemMonitor()

    def process(self, command):

        command = command.lower().strip()

        # Application control

        if "open notepad" in command:
            return self.system.open_notepad()

        elif "open calculator" in command:
            return self.system.open_calculator()

        elif "open youtube" in command:
            return self.system.open_youtube()

        # Date and time

        elif "time" in command:
            return self.system.get_time()

        elif "date" in command:
            return self.system.get_date()

        # System monitoring

        elif "cpu" in command:
            return self.monitor.get_cpu_usage()

        elif "ram" in command or "memory" in command:
            return self.monitor.get_memory_usage()

        elif "battery" in command:
            return self.monitor.get_battery_status()

        elif "disk" in command or "storage" in command:
            return self.monitor.get_disk_usage()

        elif "system information" in command:
            return self.monitor.get_system_information()

        # Fallback response

        else:
            return (
                "I'm sorry sir. "
                "I don't understand that command yet."
            )