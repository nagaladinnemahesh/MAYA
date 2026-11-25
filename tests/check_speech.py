import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone(
    device_index=1,
    sample_rate=48000,
    chunk_size=1024
) as source:

    print("Microphone connected.")
    print("Calibrating ambient noise...")

    recognizer.adjust_for_ambient_noise(
        source, duration=1
    )

    print("Listening...")

    try:
        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=10
        )

        print("Recognizing...")

        text = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You said: {text}")

    except sr.WaitTimeoutError:
        print("No speech detected.")

    except sr.UnknownValueError:
        print("Unable to understand speech.")

    except sr.RequestError as error:
        print(f"Service error: {error}")