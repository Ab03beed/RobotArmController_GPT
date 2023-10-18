import pyaudio
import speech_recognition as sr
import keyboard

class SpeechToText:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.rate = 44100
        self.chunk = 1024
        self.channels = 1
       

    def talk(self):
        stream = self.audio.open(format=self.format, rate=self.rate, channels=self.channels, input=True, frames_per_buffer=self.chunk)

        frames = []

        print("\nPress 'T' to talk or 'ESC' to exit...")
        key = keyboard.read_hotkey() #Wait for user to press a key

        if(key == 't'):
            print("Listning...  Press 'I' to interrupt")
            while True:
                data = stream.read(self.chunk)
                frames.append(data)
                if keyboard.is_pressed('I'):
                    print("Interrupted!")
                    break
        elif(key == 'esc'):
            print("Good bye!")
            return "exit"

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Convert the recorded frames to an AudioData instance
        audio_data = sr.AudioData(b''.join(frames), self.rate, self.audio.get_sample_size(self.format))

        return self._convertAudioToText(audio_data)

    def _convertAudioToText(self, audio):
        try:
            text = self.recognizer.recognize_google(audio).lower()
            print("I've heard: ", text, '\n') 
            return text
        except sr.UnknownValueError:
            # Handle unrecognized audio
            print("Couldn't understand what you said")
            return "none"
        except sr.RequestError:
            # Handle request errors
            print("Could not request results from the speech recognition service.")
            return "none"
        