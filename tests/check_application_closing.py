from tools.application_manager import ApplicationManager


manager = ApplicationManager()


print("\nNotepad Windows:")

windows = manager.get_application_windows("notepad")

for window in windows:
    print(window)


print("\nWithout Confirmation:")

print(manager.close_application("notepad"))


print("\nProtected Application Test:")

print(
    manager.close_application(
        "file explorer",
        confirmed=True
    )
)


print("\nGraceful Closing Test:")

confirmation = input(
    "Close all detected Notepad windows? (yes/no): "
)

if confirmation.lower().strip() == "yes":

    print(
        manager.close_application(
            "notepad",
            confirmed=True
        )
    )

else:
    print("Application closing cancelled.")