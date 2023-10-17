import assemblyai as aai
import time


aai.settings.api_key = f"42ebba2a84704b85b0407644635586c2"

FILE_URL = "./voiceCommand.wav"

transcriber = aai.Transcriber()

total = 0

for i in range(10):
    startTime = time.time()
    transcript = transcriber.transcribe(FILE_URL)
    endTime = time.time()
    res = endTime - startTime
    total += res
    print(i, ": ", res)

meanTime =  total / 10

print("mean time is: ", meanTime)
