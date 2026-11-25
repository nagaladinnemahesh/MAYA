import pyttsx3

from config.settings import (
    VOICE_NAME,
    VOICE_RATE,
    VOICE_VOLUME
)


class TextToSpeech:

    def __init__(self):
        self.engine = pyttsx3.init("sapi5")

        self.set_voice(VOICE_NAME)

        self.engine.setProperty("rate", VOICE_RATE)
        self.engine.setProperty("volume", VOICE_VOLUME)

    def set_voice(self, voice_name):
        voices = self.engine.getProperty("voices")

        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                self.engine.setProperty("voice", voice.id)
                print(f"Voice initialized: {voice.name}")
                return

        raise RuntimeError(
            f"Preferred voice '{voice_name}' not found."
        )

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()