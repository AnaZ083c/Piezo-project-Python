from playsound import playsound
from pydub import AudioSegment
from pydub.playback import  play

import keyboard
import pyaudio
import wave
import time

frame_rate = int(48000)
frames_per_buff = int(1024)
format = pyaudio.paInt16
channels = 2

audio = pyaudio.PyAudio()

def get_input_devices(audio):
    pyaudio.Stream.input_device_index = 2
    print(audio.get_default_input_device_info())
    for i in range(audio.get_device_count()):#list all available audio devices
      dev = audio.get_device_info_by_index(i)
      print((i,dev['name'],dev['maxInputChannels']))

get_input_devices(audio)

stream = audio.open(format=format, input_device_index=2, channels=channels, rate=frame_rate, input=True, frames_per_buffer=frames_per_buff)

frames = []

while not keyboard.is_pressed('q'):
    data = stream.read(frames_per_buff)
    frames.append(data)

stream.stop_stream()
stream.close()
audio.terminate()

sound_file = wave.open("rec32.wav", "wb")
sound_file.setnchannels(channels)
sound_file.setsampwidth(audio.get_sample_size(format))
sound_file.setframerate(frame_rate)
sound_file.writeframes(b''.join(frames))
sound_file.close()

print("Opening file")

time.sleep(1)

wav = AudioSegment.from_wav("rec32.wav")
play(wav)
