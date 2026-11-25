from config.settings import ASSISTANT_NAME, VERSION
from voice.text_to_speech import TextToSpeech
from voice.speech_to_text import SpeechToText


class Maya:

    def __init__(self):
        self.name = ASSISTANT_NAME
        self.version = VERSION

        self.voice = TextToSpeech()
        self.ears = SpeechToText()

        self.running = True

    def speak(self, message):
        print(f"{self.name}: {message}")
        self.voice.speak(message)

    def start(self):
        print(f"Initializing {self.name}...")
        print(f"Version: {self.version}")

        self.ears.calibrate()

        self.speak(
            "Hello sir. All systems are ready."
        )

        try:
            while self.running:

                command = self.ears.listen()

                if command is None:
                    continue

                print(f"You: {command}")

                if command.lower().strip() in [
                    "exit",
                    "goodbye",
                    "stop",
                    "shutdown maya"
                ]:
                    self.speak("Goodbye sir.")
                    self.running = False

                else:
                    self.speak(f"You said {command}")

        except KeyboardInterrupt:
            self.running = False
            self.speak("Shutting down. Goodbye sir.")