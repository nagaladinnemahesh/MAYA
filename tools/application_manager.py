
import os
import shutil
import subprocess
import psutil
import win32gui
import win32con
import win32process

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

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return "Sir, this application is not registered."

        if application is self.applications["explorer"]:
            return (
                "Sir, File Explorer is protected "
                "from application closing."
            )

        if application is self.applications["task_manager"]:
            return (
                "Sir, Task Manager is protected "
                "from application closing."
            )

        if confirmed is not True:
            return (
                f"Sir, closing {application['name']} "
                "may affect unsaved work. "
                "Confirmation is required."
            )

        if not windows:
            return (
                "Sir, no approved window snapshots "
                "are available."
            )

        # Validate all approved windows
        for window in windows:

            if not self.validate_window(
                window,
                application_name
            ):
                return (
                    "Sir, the approved windows have changed. "
                    "Closing operation cancelled. "
                    "Please request the action again."
                )

        requested = 0

        for window in windows:

            try:

                # Revalidate immediately before execution
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

                requested += 1

            except (OSError, win32gui.error) as error:
                print(f"Window closing error: {error}")

        if requested == 0:
            return (
                f"Sir, I could not request "
                f"{application['name']} to close."
            )

        return (
            f"Sir, I have requested {requested} of "
            f"{len(windows)} approved "
            f"{application['name']} windows to close. "
            "Please check for any save prompts."
        )
