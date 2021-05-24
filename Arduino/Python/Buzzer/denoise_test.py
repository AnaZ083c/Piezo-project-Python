import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

plt.rcParams['figure.dpi'] = 100
plt.rcParams['figure.figsize'] = (9, 7)

sampFreq, sound = wavfile.read('rec32.wav')

sound = sound / 2.0**15
length_in_s = sound.shape[0]/sampFreq
print(length_in_s)

# plotting the sound signal on each channel; I have 2 channels
# plt.subplot(2,1,1)
# plt.plot(sound[:,0], 'r')
# plt.xlabel("left channel, sample #")
# plt.subplot(2,1,2)
# plt.plot(sound[:,1], 'b')
# plt.xlabel("right channel, sample #")
# plt.tight_layout()
#plt.show()

time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s
# plt.subplot(2,1,1)
# plt.plot(time, sound[:,0], 'r')
# plt.xlabel("time, s [left channel]")
# plt.ylabel("signal, relative units")
# plt.subplot(2,1,2)
# plt.plot(time, sound[:,1], 'b')
# plt.xlabel("time, s [right channel]")
# plt.ylabel("signal, relative units")
# plt.tight_layout()
# plt.show()

# work only with one channel
signal = sound[:,0]
# plt.plot(time[60:70], signal[60:70])
# plt.xlabel("time, s")
# plt.ylabel("Signal, relative units")
# plt.show()

fft_spectrum = np.fft.rfft(signal)
freq = np.fft.rfftfreq(signal.size, d=1./sampFreq)
fft_spectrum_abs = np.abs(fft_spectrum) # absolute values of fft_spectrum, since they are unreal numbers

# plt.plot(freq, fft_spectrum_abs)
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()

# plt.plot(freq[:3000], fft_spectrum_abs[:3000])
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()

for i,f in enumerate(freq):
    if f < 62 and f > 58:# (1)
        fft_spectrum[i] = 0.0
    if f < 21 or f > 20000:# (2)
        fft_spectrum[i] = 0.0

plt.plot(freq[:3000], np.abs(fft_spectrum[:3000]))
plt.xlabel("frequency, Hz")
plt.ylabel("Amplitude, units")
plt.show()

noiseless_signal = np.fft.irfft(fft_spectrum)
wavfile.write("noisless-rec32.wav", sampFreq, noiseless_signal)