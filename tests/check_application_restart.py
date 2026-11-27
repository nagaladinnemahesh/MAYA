from tools.application_manager import ApplicationManager


manager = ApplicationManager()


print("\nTest 1: Unknown application")

print(
    manager.restart_application("unknown_app")
)


print("\nTest 2: Protected application")

print(
    manager.restart_application(
        "explorer",
        confirmed=True
    )
)


print("\nTest 3: Confirmation required")

print(
    manager.restart_application("notepad")
)


print("\nTest 4: No approved windows")

print(
    manager.restart_application(
        "notepad",
        confirmed=True,
        windows=[]
    )
)


print("\nTest 5: Application restart")

print(manager.open_application("notepad"))

input("Ensure Notepad is open, then press Enter: ")

windows = manager.get_application_windows("notepad")

print("Approved windows:", windows)

confirmation = input("Confirm restart? (yes/no): ")

if confirmation.lower().strip() == "yes":

    print(
        manager.restart_application(
            "notepad",
            confirmed=True,
            windows=windows
        )
    )

else:

    print("Restart cancelled.")