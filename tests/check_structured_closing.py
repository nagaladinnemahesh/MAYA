from tools.application_manager import ApplicationManager


manager = ApplicationManager()


print("\nTest 1: Unknown application")

print(
    manager.request_application_close(
        "unknown_app"
    )
)


print("\nTest 2: Protected application")

print(
    manager.request_application_close(
        "explorer",
        confirmed=True
    )
)


print("\nTest 3: Confirmation required")

print(
    manager.request_application_close(
        "notepad"
    )
)


print("\nTest 4: No approved windows")

print(
    manager.request_application_close(
        "notepad",
        confirmed=True,
        windows=[]
    )
)


print("\nTest 5: Successful closing request")

print(manager.open_application("notepad"))

input("Ensure Notepad is open, then press Enter: ")

windows = manager.get_application_windows("notepad")

print("Captured windows:", windows)

confirmation = input("Confirm closing? (yes/no): ")

if confirmation.lower().strip() == "yes":

    result = manager.request_application_close(
        "notepad",
        confirmed=True,
        windows=windows
    )

    print(result)

else:

    print("Test cancelled.")