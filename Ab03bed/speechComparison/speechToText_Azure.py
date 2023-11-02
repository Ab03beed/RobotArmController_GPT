import azure.cognitiveservices.speech as speechsdk
import os
import time

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
speech_config.speech_recognition_language="en-US"

audio_config = speechsdk.audio.AudioConfig(filename='C:/Users/abdah/OneDrive/Documents/GitHub/SIMS/Ab03bed/speechComparison/voiceCommand.wav')
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

total = 0

# Open the audio file outside the loop to avoid reopening it multiple times
for i in range(10):
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_config.speech_recognition_language="en-US"
    audio_config = speechsdk.audio.AudioConfig(filename='C:/Users/abdah/OneDrive/Documents/GitHub/SIMS/Ab03bed/speechComparison/voiceCommand.wav')
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    startTime = time.time()
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    endTime = time.time()
    res = endTime - startTime
    total += res
    print("Recognized: {}".format(speech_recognition_result.text))
    print(i, ": ", res)
    time.sleep(1)

meanValue =  total / 10

print("mean value is: ", meanValue)