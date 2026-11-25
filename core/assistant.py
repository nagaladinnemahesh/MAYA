from config.settings import ASSISTANT_NAME, VERSION
from voice.text_to_speech import TextToSpeech


class Maya:

    def __init__(self):
        self.name = ASSISTANT_NAME
        self.version = VERSION
        self.voice = TextToSpeech()

    def start(self):
        print(f"Initializing {self.name}...")
        print(f"Version: {self.version}")

        message = f"Hello, I am {self.name}. How can I assist you?"

        print(message)
        self.voice.speak(message)