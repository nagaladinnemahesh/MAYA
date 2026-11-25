import time

from core.confirmation_manager import ConfirmationManager


manager = ConfirmationManager(timeout=3)


print("\nTest 1: Initial State")

print(manager.has_pending_action())


print("\nTest 2: Request Confirmation")

manager.request_confirmation(
    "close_application",
    {"application_name": "brave"}
)

print(manager.has_pending_action())


print("\nTest 3: Confirm Action")

print(manager.confirm())

print(manager.has_pending_action())


print("\nTest 4: Cancel Action")

manager.request_confirmation(
    "close_application",
    {"application_name": "notepad"}
)

print(manager.cancel())

print(manager.has_pending_action())


print("\nTest 5: Confirmation Timeout")

manager.request_confirmation(
    "close_application",
    {"application_name": "vscode"}
)

print("Waiting for confirmation to expire...")

time.sleep(4)

print(manager.has_pending_action())


print("\nTest 6: Confirm Without Pending Action")

print(manager.confirm())