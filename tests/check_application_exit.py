from tools.application_manager import ApplicationManager


manager = ApplicationManager()


print("\nTest 1: Application already closed")

print(
    manager.wait_for_application_exit("notepad")
)


print("\nTest 2: Application still running")

print(manager.open_application("notepad"))

input("Wait for Notepad to open, then press Enter: ")

print(
    manager.wait_for_application_exit(
        "notepad",
        timeout=5
    )
)


print("\nTest 3: Close application during polling")

input("Press Enter, then manually close Notepad within 10 seconds: ")

print(
    manager.wait_for_application_exit(
        "notepad",
        timeout=10
    )
)


print("\nTest 4: Unregistered application")

print(
    manager.wait_for_application_exit("unknown_app")
)