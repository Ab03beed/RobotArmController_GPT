import speech_recognition as sr
import time
from os import path

total = 0

audio = path.join(path.dirname(path.realpath(__file__)), "voiceCommand.wav")


recognizer = sr.Recognizer()

with sr.AudioFile(audio) as source:
    audio = recognizer.record(source)  # read the entire audio file


"""with sr.Microphone() as mic:
    print("Which box should I move?")
    
    audio = recognizer.listen(mic)

with open("voiceCommand.wav", "wb") as f: 
    f.write(audio.get_wav_data())

startTime = time.time()
text = recognizer.recognize_google(audio).lower()
endTime = time.time()

res = endTime - startTime

print("I've heard: ", text, "\nTime: ", res) 
"""

for i in range(10):
    startTime = time.time()
    text = recognizer.recognize_google(audio).lower()
    endTime = time.time()
    res = endTime - startTime
    total += res
    print(i, ": ", res)

meanValue =  total / 10

print("mean value is: ", meanValue)

