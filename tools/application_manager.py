
import os
import shutil
import subprocess
import psutil
import win32gui
import win32con
import win32process
import time

from config.applications import APPLICATIONS


class ApplicationManager:

    def __init__(self):
        self.applications = APPLICATIONS

    def resolve_application(self, application_name):

        application_name = application_name.lower().strip()

        for key, application in self.applications.items():

            if (
                application_name == key
                or application_name in application["aliases"]
            ):
                return application

        return None

    def find_executable(self, application):

        # Strategy 1: Search registered paths

        for path in application["paths"]:

            if os.path.isabs(path):

                if os.path.isfile(path):
                    return path

            elif os.path.basename(path) == path:

                executable = shutil.which(path)

                if executable:
                    return executable

        # Strategy 2: Discover from running processes

        process_names = {
            name.lower()
            for name in application["process_names"]
        }

        for process in psutil.process_iter(["name", "exe"]):

            try:
                name = process.info["name"]
                executable = process.info["exe"]

                if (
                    name
                    and name.lower() in process_names
                    and executable
                    and os.path.isabs(executable)
                    and os.path.isfile(executable)
                    and os.path.basename(executable).lower()
                    in process_names
                ):
                    return executable

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        return None

    def open_application(self, application_name):

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return (
                f"Sir, {application_name} is not "
                "registered in my application registry."
            )

        executable = self.find_executable(application)

        if executable is None:
            return (
                f"Sir, I could not locate "
                f"{application['name']} on your system."
            )

        try:
            subprocess.Popen([executable])

            return f"Opening {application['name']}, sir."

        except OSError as error:

            print(f"Application launch error: {error}")

            return (
                f"Sir, I was unable to open "
                f"{application['name']}."
            )

    def is_application_running(self, application_name):

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return None

        process_names = {
            name.lower()
            for name in application["process_names"]
        }

        for process in psutil.process_iter(["name"]):

            try:
                name = process.info["name"]

                if name and name.lower() in process_names:
                    return True

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess
            ):
                continue

        return False

    def get_running_applications(self):

        running_applications = []

        for key, application in self.applications.items():

            if self.is_application_running(key):

                running_applications.append({
                    "key": key,
                    "name": application["name"]
                })

        return running_applications

    def get_application_windows(self, application_name):

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return []

        process_names = {
            name.lower()
            for name in application["process_names"]
        }

        windows = []

        def enum_callback(hwnd, _):

            try:
                if not win32gui.IsWindowVisible(hwnd):
                    return True

                title = win32gui.GetWindowText(hwnd)

                if not title:
                    return True

                _, pid = win32process.GetWindowThreadProcessId(
                    hwnd
                )

                process = psutil.Process(pid)

                if process.name().lower() in process_names:

                    windows.append({
                        "hwnd": hwnd,
                        "pid": pid,
                        "title": title,
                        "created_at": process.create_time()
                    })

            except (psutil.Error, OSError, win32gui.error):
                pass

            return True

        win32gui.EnumWindows(enum_callback, None)

        return windows
    
    def validate_window(self, window, application_name):

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return False

        process_names = {
            name.lower()
            for name in application["process_names"]
        }

        try:

            hwnd = window["hwnd"]

            if not win32gui.IsWindow(hwnd):
                return False

            if not win32gui.IsWindowVisible(hwnd):
                return False

            _, pid = win32process.GetWindowThreadProcessId(
                hwnd
            )

            if pid != window["pid"]:
                return False

            process = psutil.Process(pid)

            if process.name().lower() not in process_names:
                return False

            if process.create_time() != window["created_at"]:
                return False

            return True

        except (psutil.Error, OSError, win32gui.error):
            return False

    def close_application(
        self,
        application_name,
        confirmed=False,
        windows=None
    ):

        result = self.request_application_close(
            application_name=application_name,
            confirmed=confirmed,
            windows=windows
        )

        application = self.resolve_application(
            application_name
        )

        if result["error"] == "application_not_registered":
            return "Sir, this application is not registered."

        application_display_name = application["name"]

        if result["error"] == "protected_application":
            return (
                f"Sir, {application_display_name} is protected "
                "from application closing."
            )

        if result["error"] == "confirmation_required":
            return (
                f"Sir, closing {application_display_name} "
                "may affect unsaved work. "
                "Confirmation is required."
            )

        if result["error"] == "no_approved_windows":
            return (
                "Sir, no approved window snapshots "
                "are available."
            )

        if result["error"] == "window_validation_failed":
            return (
                "Sir, the approved windows have changed. "
                "Closing operation cancelled. "
                "Please request the action again."
            )

        if result["error"] == "close_request_failed":
            return (
                f"Sir, I could not request "
                f"{application_display_name} to close."
            )

        if result["error"] == "partial_close_request":
            return (
                f"Sir, only {result['requested']} of "
                f"{result['total']} approved "
                f"{application_display_name} windows "
                "received closing requests. "
                "Please check the remaining windows."
            )

        if result["success"]:
            return (
                f"Sir, I have requested "
                f"{result['requested']} of "
                f"{result['total']} approved "
                f"{application_display_name} windows to close. "
                "Please check for any save prompts."
            )

        return "Sir, an unexpected closing error occurred."
    
    def wait_for_application_exit(
        self,
        application_name,
        timeout=5
    ):

        start_time = time.monotonic()

        while time.monotonic() - start_time < timeout:

            running = self.is_application_running(
                application_name
            )

            if running is False:
                return True

            if running is None:
                return False

            time.sleep(0.5)

        return (
            self.is_application_running(application_name)
            is False
        )
    def request_application_close(
        self,
        application_name,
        confirmed=False,
        windows=None
    ):

        result = {
            "success": False,
            "requested": 0,
            "total": len(windows) if windows else 0,
            "error": None
        }

        application = self.resolve_application(
            application_name
        )

        if application is None:
            result["error"] = "application_not_registered"
            return result

        if application["name"] in [
            "File Explorer",
            "Task Manager"
        ]:
            result["error"] = "protected_application"
            return result

        if confirmed is not True:
            result["error"] = "confirmation_required"
            return result

        if not windows:
            result["error"] = "no_approved_windows"
            return result

        for window in windows:

            if not self.validate_window(
                window,
                application_name
            ):
                result["error"] = "window_validation_failed"
                return result

        for window in windows:

            try:

                if not self.validate_window(
                    window,
                    application_name
                ):
                    continue

                win32gui.PostMessage(
                    window["hwnd"],
                    win32con.WM_CLOSE,
                    0,
                    0
                )

                result["requested"] += 1

            except (OSError, win32gui.error) as error:

                print(f"Window closing error: {error}")

        if result["requested"] == result["total"]:
            result["success"] = True

        elif result["requested"] == 0:
            result["error"] = "close_request_failed"

        else:
            result["error"] = "partial_close_request"

        return result
    
    def restart_application(
        self,
        application_name,
        confirmed=False,
        windows=None
    ):

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return "Sir, this application is not registered."

        display_name = application["name"]

        if display_name in [
            "File Explorer",
            "Task Manager"
        ]:
            return (
                f"Sir, {display_name} is protected "
                "from application restart."
            )

        if confirmed is not True:
            return (
                f"Sir, restarting {display_name} "
                "may affect unsaved work. "
                "Confirmation is required."
            )

        executable = self.find_executable(application)

        if executable is None:
            return (
                f"Sir, I could not locate {display_name}. "
                "Restart cancelled."
            )

        if not windows:
            return (
                "Sir, no approved window snapshots "
                "are available."
            )

        current_windows = self.get_application_windows(
            application_name
        )

        approved_identities = {
            (
                window["hwnd"],
                window["pid"],
                window["created_at"]
            )
            for window in windows
        }

        current_identities = {
            (
                window["hwnd"],
                window["pid"],
                window["created_at"]
            )
            for window in current_windows
        }

        if approved_identities != current_identities:
            return (
                "Sir, the application windows have changed. "
                "Restart cancelled. "
                "Please request the action again."
            )

        result = self.request_application_close(
            application_name=application_name,
            confirmed=True,
            windows=windows
        )

        if not result["success"]:
            return (
                f"Sir, I could not submit all closing "
                f"requests for {display_name}. "
                "Restart cancelled."
            )

        if not self.wait_for_application_exit(
            application_name,
            timeout=5
        ):
            return (
                f"Sir, {display_name} is still running. "
                "Please check for unsaved work "
                "or background processes. "
                "Restart cancelled."
            )

        if self.is_application_running(application_name) is not False:
            return (
                f"Sir, {display_name} is running again. "
                "Restart cancelled."
            )

        try:

            subprocess.Popen([executable])

            return (
                f"Sir, {display_name} has exited "
                "and a new launch has been requested."
            )

        except OSError as error:

            print(f"Application restart error: {error}")

            return (
                f"Sir, {display_name} was closed, "
                "but I was unable to relaunch it."
            )
