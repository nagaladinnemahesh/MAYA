from tools.system_tools import SystemTools
from tools.system_monitor import SystemMonitor
from tools.process_monitor import ProcessMonitor
from core.response_formatter import ResponseFormatter


class CommandProcessor:

    def __init__(self):

        self.system = SystemTools()
        self.monitor = SystemMonitor()
        self.process_monitor = ProcessMonitor()
        self.formatter = ResponseFormatter()

    def process(self, command):

        command = command.lower().strip()

        # Application control

        if "open notepad" in command:
            return self.system.open_notepad()

        elif "open calculator" in command:
            return self.system.open_calculator()

        elif "open youtube" in command:
            return self.system.open_youtube()

        # Process monitoring

        elif any(phrase in command for phrase in [
            "top memory processes",
            "top ram processes",
            "memory consuming processes",
            "using the most memory",
            "using the most ram"
        ]):

            processes = (
                self.process_monitor.get_top_memory_processes()
            )

            return self.formatter.format_memory_processes(
                processes
            )

        elif any(phrase in command for phrase in [
            "top cpu processes",
            "cpu consuming processes",
            "using the most cpu"
        ]):

            processes = (
                self.process_monitor.get_top_cpu_processes()
            )

            return self.formatter.format_cpu_processes(
                processes
            )

        elif any(phrase in command for phrase in [
            "running processes",
            "process count",
            "how many processes"
        ]):

            count = (
                self.process_monitor.get_running_process_count()
            )

            return self.formatter.format_process_count(count)

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