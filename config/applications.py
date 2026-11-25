import os


LOCAL_APP_DATA = os.environ.get("LOCALAPPDATA", "")
PROGRAM_FILES = os.environ.get("ProgramFiles", "")
PROGRAM_FILES_X86 = os.environ.get("ProgramFiles(x86)", "")


APPLICATIONS = {

    "notepad": {
        "name": "Notepad",
        "aliases": ["notepad", "text editor"],
        "paths": ["notepad.exe"],
        "process_names": ["notepad.exe"]
    },

    "calculator": {
        "name": "Calculator",
        "aliases": ["calculator", "calc"],
        "paths": ["calc.exe"],
        "process_names": ["CalculatorApp.exe", "Calculator.exe"]
    },

    "brave": {
        "name": "Brave Browser",
        "aliases": ["brave", "brave browser"],
        "paths": [
            os.path.join(
                PROGRAM_FILES,
                "BraveSoftware",
                "Brave-Browser",
                "Application",
                "brave.exe"
            ),
            os.path.join(
                PROGRAM_FILES_X86,
                "BraveSoftware",
                "Brave-Browser",
                "Application",
                "brave.exe"
            ),
            os.path.join(
                LOCAL_APP_DATA,
                "BraveSoftware",
                "Brave-Browser",
                "Application",
                "brave.exe"
            )
        ],
        "process_names": ["brave.exe"]
    },

        "vscode": {
        "name": "Visual Studio Code",
        "aliases": [
            "vs code",
            "vscode",
            "visual studio code"
        ],
        "paths": [
            os.path.join(
                LOCAL_APP_DATA,
                "Programs",
                "Microsoft VS Code",
                "Code.exe"
            ),
            os.path.join(
                LOCAL_APP_DATA,
                "Programs",
                "Microsoft VS Code",
                "_",
                "Code.exe"
            ),
            os.path.join(
                PROGRAM_FILES,
                "Microsoft VS Code",
                "Code.exe"
            ),
            os.path.join(
                PROGRAM_FILES,
                "Microsoft VS Code",
                "_",
                "Code.exe"
            ),
            "Code.exe"
        ],
        "process_names": ["Code.exe"]
    },

    "explorer": {
        "name": "File Explorer",
        "aliases": ["file explorer", "explorer"],
        "paths": ["explorer.exe"],
        "process_names": ["explorer.exe"]
    },

    "task_manager": {
        "name": "Task Manager",
        "aliases": ["task manager", "taskmgr"],
        "paths": ["taskmgr.exe"],
        "process_names": ["Taskmgr.exe"]
    }
}