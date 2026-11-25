import speech_recognition as sr

microphones = sr.Microphone.list_microphone_names()

for index, microphone in enumerate(microphones):
    print(f"Index: {index} | Device: {microphone}")