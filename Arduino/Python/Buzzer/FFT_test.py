import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

sampFreq, sound = wavfile.read('rec32.wav')
sound = sound / 2.0**15

length_in_s = sound.shape[0] / sampFreq

time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

signal = sound[:,0]


fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1./sampFreq)
fft_spectrum_abs = np.abs(fft_spectrum)

for i,f in enumerate(fft_spectrum_abs):
    if f > 350: #looking at amplitudes of the spikes higher than 350
        print('frequency = {} Hz with amplitude {} '.format(np.round(freq[i],1),  np.round(f)))

for i, f in enumerate(freq):
    if f < 62 and f > 58:  # (1)
        fft_spectrum[i] = 0.0
    if f < 21 or f > 20000:  # (2)
        fft_spectrum[i] = 0.0

print(np.round(freq, 1))
