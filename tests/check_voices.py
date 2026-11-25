import pyttsx3

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 165)

print("Requested voice:", voices[1].name)
print("Active voice:", engine.getProperty("voice"))

engine.say("Hello sir. I am Maya. All systems are ready.")
engine.runAndWait()