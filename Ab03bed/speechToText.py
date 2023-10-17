import speech_recognition as sr
import keyboard

class SpeechToText:

    #parametrized cunstructor
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    
    def talk(self):
        print("\nPress V to talk ...")
        keyboard.wait('v')
        
        with sr.Microphone() as mic:
            print("Which box should I move?")
            audio = self.recognizer.listen(mic)

        return self._convertAudioToText(audio)
       


    def _convertAudioToText(self, audio):
        try:
            text = self.recognizer.recognize_google(audio).lower()
            print("I've heard: ", text, '\n') 
            return text
        except sr.UnknownValueError:
            #Handle unrecognized audio
            print("Couldn't undersatnd the what you said")
            return "none"
        except sr.RequestError:
            # Handle request errors
            print("Could not request results from the speech recognition service.")
            return "none"
                