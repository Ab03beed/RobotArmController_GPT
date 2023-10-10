import speech_recognition as sr

class SpeechToText:

    #parametrized cunstructor
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    
    def talk(self):
        with sr.Microphone() as mic:
            print("I'm listening...")
            audio = self.recognizer.listen(mic)

        return self._convertAudioToText(audio)
       


    def _convertAudioToText(self, audio):
        try:
            text = self.recognizer.recognize_google(audio).lower()
            print("I've heard: ", text) 
            return text
        except sr.UnknownValueError:
            #Handle unrecognized audio
            #print("Could not understand the audio.")
            return "none"
        except sr.RequestError:
            # Handle request errors
            print("Could not request results from the speech recognition service.")
            return "none"        
