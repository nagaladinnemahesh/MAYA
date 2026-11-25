
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
                        "title": title
                    })

            except (psutil.Error, OSError, win32gui.error):
                pass

            return True

        win32gui.EnumWindows(enum_callback, None)

        return windows

    def close_application(
        self, application_name, confirmed=False
    ):

        application = self.resolve_application(
            application_name
        )

        if application is None:
            return "Sir, this application is not registered."

        # Protect Windows system applications

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

        # Require confirmation before closing

        if confirmed is not True:
            return (
                f"Sir, closing {application['name']} "
                "may affect unsaved work. "
                "Confirmation is required."
            )

        windows = self.get_application_windows(
            application_name
        )

        if not windows:
            return (
                f"Sir, no matching visible windows were "
                f"found for {application['name']}."
            )

        requested = 0

        # Request graceful window closing

        for window in windows:

            try:
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
            f"Sir, I have requested {requested} "
            f"{application['name']} windows to close. "
            "Please check for any save prompts."
        )
