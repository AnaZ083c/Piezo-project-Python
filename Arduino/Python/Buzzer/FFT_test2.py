import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fftpack import fft
import numpy as np
#import melodia
import librosa

wave_data, samplerate=librosa.load("recording.wav")

plt.subplot(211)
plt.plot(wave_data)
plt.title('wave')
pitches, magnitudes = librosa.piptrack(y=wave_data, sr=samplerate)
plt.subplot(212)
plt.imshow(pitches[:100, :], aspect="auto", interpolation="nearest", origin="lower")
plt.title('pitches')
plt.show()

