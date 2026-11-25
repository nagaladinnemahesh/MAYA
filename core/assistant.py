from config.settings import ASSISTANT_NAME, VERSION


class Maya:

    def __init__(self):
        self.name = ASSISTANT_NAME
        self.version = VERSION

    def start(self):
        print(f"Initializing {self.name}...")
        print(f"Version: {self.version}")
        print(f"Hello, I am {self.name}. How can I assist you?")