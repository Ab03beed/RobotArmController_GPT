import speech_recognition as sr

class SpeechToText:

    #parametrized cunstructor
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    
    def talk(self):
        with sr.Microphone() as mic:
            audio = self.recognizer.listen(mic)
        
        return self._convertAudioToText(audio)


    def _convertAudioToText(self, audio):
        try:
            return self.recognizer.recognize_google(audio).lower()
        except:
            print("Couldn't understand what you've said")