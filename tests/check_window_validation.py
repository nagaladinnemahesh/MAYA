from tools.application_manager import ApplicationManager


manager = ApplicationManager()


print("\nTest 1: Capture Notepad Windows")

windows = manager.get_application_windows("notepad")

for window in windows:
    print(window)


print("\nTest 2: Validate Captured Windows")

for window in windows:

    valid = manager.validate_window(
        window,
        "notepad"
    )

    print(f"{window['title']}: {valid}")


print("\nTest 3: Invalid Process ID")

if windows:

    invalid_window = windows[0].copy()

    invalid_window["pid"] = -1

    print(
        manager.validate_window(
            invalid_window,
            "notepad"
        )
    )


print("\nTest 4: Invalid Creation Time")

if windows:

    invalid_window = windows[0].copy()

    invalid_window["created_at"] = 0

    print(
        manager.validate_window(
            invalid_window,
            "notepad"
        )
    )


print("\nTest 5: Stale Window Validation")

input("Close Notepad manually, then press Enter: ")

for window in windows:

    print(
        manager.validate_window(
            window,
            "notepad"
        )
    )