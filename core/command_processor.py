
from tools.system_tools import SystemTools
from tools.system_monitor import SystemMonitor
from tools.process_monitor import ProcessMonitor
from tools.application_manager import ApplicationManager

from core.response_formatter import ResponseFormatter
from core.confirmation_manager import ConfirmationManager


class CommandProcessor:

    def __init__(
            self):

        self.system = SystemTools()
        self.monitor = SystemMonitor()
        self.process_monitor = ProcessMonitor()
        self.formatter = ResponseFormatter()

        self.application_manager = ApplicationManager()
        self.confirmation_manager = ConfirmationManager(
            timeout=30
        )

    def process(self, command):

        command = command.lower().strip()

        # Confirmation handling

        if command in [
            "confirm",
            "yes proceed",
            "yes, proceed",
            "confirm action"
        ]:

            action = self.confirmation_manager.confirm()

            if action is None:
                return (
                    "Sir, there is no active action "
                    "awaiting confirmation."
                )

            return self.execute_confirmed_action(action)

        # Cancellation handling

        if command in [
            "no",
            "cancel",
            "cancel action",
            "do not proceed"
        ]:

            if self.confirmation_manager.cancel():
                return "Action cancelled, sir."

            return "Sir, there is no pending action."

        # Cancel pending actions when a new command arrives

        if self.confirmation_manager.has_pending_action():

            self.confirmation_manager.clear()

            return (
                "Sir, the previous action has been cancelled. "
                "Please repeat your new command."
            )

        # Website control

        if command == "open youtube":
            return self.system.open_youtube()

        # Application opening

        elif command.startswith("open "):

            application_name = command[5:].strip()

            return self.application_manager.open_application(
                application_name
            )

        # Application closing

        elif command.startswith("close "):

            application_name = command[6:].strip()

            application = (
                self.application_manager.resolve_application(
                    application_name
                )
            )

            if application is None:
                return (
                    f"Sir, {application_name} is not "
                    "registered in my application registry."
                )

            if application["name"] in [
                "File Explorer",
                "Task Manager"
            ]:
                return (
                    f"Sir, {application['name']} is protected "
                    "from application closing."
                )

            windows = (
                self.application_manager.get_application_windows(
                    application_name
                )
            )

            if not windows:
                return (
                    f"Sir, no matching visible windows were "
                    f"found for {application['name']}."
                )

            self.confirmation_manager.request_confirmation(
                "close_application",
                {"application_name": application_name,
                 "windows": windows}
            )

            return (
                f"Sir, closing {application['name']} "
                "may affect unsaved work. "
                "Say confirm or cancel."
            )

        # Running application listing

        elif command in [
            "running applications",
            "list running applications",
            "which applications are running",
            "show running applications"
        ]:

            applications = (
                self.application_manager.get_running_applications()
            )

            if not applications:
                return (
                    "Sir, no registered applications "
                    "are currently running."
                )

            names = ", ".join(
                application["name"]
                for application in applications
            )

            return (
                f"Sir, the following registered applications "
                f"are running: {names}."
            )

        # Individual application status

        elif command.startswith("is ") and command.endswith(
            " running"
        ):

            application_name = command[3:-8].strip()

            running = (
                self.application_manager.is_application_running(
                    application_name
                )
            )

            if running is None:
                return "Sir, this application is not registered."

            if running:
                return (
                    f"Yes sir, {application_name} "
                    "is currently running."
                )

            return (
                f"No sir, {application_name} "
                "is not currently running."
            )

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

    def execute_confirmed_action(self, action):

        action_name = action["action"]
        parameters = action["parameters"]

        if action_name == "close_application":

            return self.application_manager.close_application(
                application_name=parameters["application_name"],
                confirmed=True,
                windows=parameters["windows"]
            )

        return "Sir, this action is not supported."
