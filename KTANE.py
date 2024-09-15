import os
from vosk import Model, KaldiRecognizer
import pyaudio

model = Model('C:\\Users\\alexx\\Desktop\\KTANE')

p = pyaudio.PyAudio()

recognizer = KaldiRecognizer(model, 16000)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
stream.start_stream()

print("Listening...")
while stream.is_active():
    data = stream.read(8192,exception_on_overflow=False)
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        print("Accepted")
        print(result)