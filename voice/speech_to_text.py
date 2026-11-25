import speech_recognition as sr

from config.settings import (
    MICROPHONE_INDEX,
    SPEECH_LANGUAGE,
    LISTEN_TIMEOUT,
    PHRASE_TIME_LIMIT,
    AMBIENT_NOISE_DURATION
)


class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()

        self.microphone = sr.Microphone(
            device_index=MICROPHONE_INDEX
        )

    def calibrate(self):
        with self.microphone as source:
            print("Calibrating ambient noise...")

            self.recognizer.adjust_for_ambient_noise(
                source,
                duration=AMBIENT_NOISE_DURATION
            )

            print("Calibration completed.")

    def listen(self):
        try:
            with self.microphone as source:

                print("Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=LISTEN_TIMEOUT,
                    phrase_time_limit=PHRASE_TIME_LIMIT
                )

            print("Recognizing...")

            text = self.recognizer.recognize_google(
                audio,
                language=SPEECH_LANGUAGE
            )

            return text

        except sr.WaitTimeoutError:
            return None

        except sr.UnknownValueError:
            print("Unable to understand speech.")
            return None

        except sr.RequestError as error:
            print(f"Recognition service error: {error}")
            return None