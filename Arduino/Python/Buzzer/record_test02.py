import sounddevice as sd

from scipy.io.wavfile import write

def record_wav():
    fs = 44100 # sample rate
    seconds = 3 # duration of recording

    myrec = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, myrec)