import azure.cognitiveservices.speech as speechsdk
import os
import keyboard
import time

class SpeechToText:

    def __init__(self):
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        speech_config.speech_recognition_language="en-US"
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)


    def talk(self):
        commands = ['t','esc']
        print("\nPress 'T' to talk or 'ESC' to exit...")
        #key = keyboard.read_event(suppress=True) #Wait for user to press a key
        
        command = ""
        while command not in commands:
            key = keyboard.read_event(suppress=True) #Wait for user to press a key
            command = key.name

            if(command == 't'):
                print("Listning...")
                speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
                if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    print("Recognized: {}".format(speech_recognition_result.text))
                else:
                    return 'none'
            elif(command == 'esc'):
                print("Good bye!")
                return "exit"
            else:
                print("Invaild command --> Press 'T' to talk or 'ESC' to exit...")
                time.sleep(0.5)

        print(speech_recognition_result.text)
        return speech_recognition_result.text.lower()
    