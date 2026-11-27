import time


class ConfirmationManager:

    def __init__(self, timeout=30):

        self.pending_action = None
        self.timeout = timeout

    def request_confirmation(self, action, parameters):

        self.pending_action = {
            "action": action,
            "parameters": parameters.copy(),
            "created_at": time.monotonic()
        }

    def has_pending_action(self):

        if self.pending_action is None:
            return False

        elapsed_time = (
            time.monotonic()
            - self.pending_action["created_at"]
        )

        if elapsed_time >= self.timeout:

            self.clear()

            return False

        return True

    def confirm(self):

        if not self.has_pending_action():
            return None

        action = self.pending_action

        self.clear()

        return action

    def cancel(self):

        if not self.has_pending_action():
            return False

        self.clear()

        return True

    def clear(self):

        self.pending_action = None