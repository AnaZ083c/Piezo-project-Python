from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import numpy as np
import keyboard
import pyaudio
import wave
import time

from scipy.interpolate import interp1d
from scipy.io import wavfile
from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play

# instantiate PyMata3
board = PyMata3(com_port='com6')

# Arduino PIN settup
GREEN_LED = 12
RED_LED = 8
REC_BUTTON = 2
PLAY_BUTTON = 7
YELLOW_LED = 4
BUZZER = 10

# REC init
rec_button_pushed = 0
rec_led_state = 0
rec_previous_button_state = 0
rec_last_debounce_time = 0.0
rec_debounce_delay = 150.0
rec_times_pressed = 0

# PLAY init
play_button_pushed = 0
play_led_state = 0
play_previous_button_state = 0
play_last_debounce_time = 0.0
play_debounce_delay = 150.0
play_times_pressed = 0

rec = {"reading": 0,
       "button_pushed": 0,
       "led_state": 0,
       "previous_button_state": 0,
       "last_debounce_time": 0,
       "debounce_delay": 150.0,
       "times_pressed": 0,
       "frequencies": []}

_play = {"reading": 0,
         "button_pushed": 0,
         "led_state": 0,
         "previous_button_state": 0,
         "last_debounce_time": 0,
         "debounce_delay": 150.0,
         "times_pressed": 0}


def setup():
    board.set_pin_mode(REC_BUTTON, Constants.INPUT)
    board.set_pin_mode(PLAY_BUTTON, Constants.INPUT)

    board.set_pin_mode(GREEN_LED, Constants.OUTPUT)
    board.set_pin_mode(RED_LED, Constants.OUTPUT)
    board.set_pin_mode(YELLOW_LED, Constants.OUTPUT)
    board.set_pin_mode(BUZZER, Constants.OUTPUT)

    # board.digital_write(RED_LED, rec["led_state"])
    # board.digital_write(GREEN_LED, _play["led_state"])

def loop():
    # board.digital_write(YELLOW_LED, 0)
    # board.sleep(5)
    # board.digital_write(YELLOW_LED, 1)
    # board.sleep(5)
    # board.play_tone(BUZZER, Constants.TONE_NO_TONE, 0, 0)

    reading_rec = board.digital_read(REC_BUTTON)
    reading_play = board.digital_read(PLAY_BUTTON)
    wav_filename = "recording.wav"

    # REC ====================
    if _play["led_state"] != 1:
        if reading_rec != rec["previous_button_state"]:
            rec["last_debonce_time"] = float(time.time() / 1000)

        if ((time.time() / 1000) - rec["last_debounce_time"]) > rec["debounce_delay"]:
            if reading_rec != rec["button_pushed"]:
                rec["button_pushed"] = reading_rec
            if rec["button_pushed"] == 1:
                rec["led_state"] = int(not bool(rec["led_state"]))

        board.digital_write(RED_LED, rec["led_state"])
        rec["previous_button_state"] = reading_rec

    # PLAY ===================
    if rec["led_state"] != 1:
        if reading_play != _play["previous_button_state"]:
            _play["last_debonce_time"] = float(time.time() / 1000)

        if ((time.time() / 1000) - _play["last_debounce_time"]) > _play["debounce_delay"]:
            if reading_play != _play["button_pushed"]:
                _play["button_pushed"] = reading_play
            if _play["button_pushed"] == 1:
                _play["led_state"] = int(not bool(_play["led_state"]))

        board.digital_write(GREEN_LED, _play["led_state"])
        _play["previous_button_state"] = reading_play

    if rec["led_state"] == 1:
        board.sleep(2)

        frame_rate = int(48000)
        frames_per_buff = int(1024)
        format = pyaudio.paInt16
        channels = 2

        audio = pyaudio.PyAudio()
        # pyaudio.Stream.input_device_index = 2
        # default_input_dev = audio.get_default_input_device_info()
        # print(default_input_dev['index'], default_input_dev['name'], default_input_dev['maxInputChannels'])
        # for i in range(audio.get_device_count()):  # list all available audio devices
        #     dev = audio.get_device_info_by_index(i)
        #     print((i, dev['name'], dev['maxInputChannels']))

        print(20 * '=')
        print('RECORDING ...')

        stream = audio.open(format=format, input_device_index=2, channels=channels, rate=frame_rate, input=True,
                            frames_per_buffer=frames_per_buff)

        frames = []

        while True:
            reading_rec = board.digital_read(REC_BUTTON)
            data = stream.read(frames_per_buff)
            frames.append(data)
            if reading_rec == 1:
                print('STOPPED ...')
                print(20 * '=')
                break

        print("Saving file as '" + wav_filename + "' ...")
        board.digital_write(YELLOW_LED, 1)
        rec["led_state"] = int(not bool(rec["led_state"]))
        board.digital_write(RED_LED, rec["led_state"])
        board.sleep(2)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open(wav_filename, 'wb')
        sound_file.setnchannels(channels)
        sound_file.setsampwidth(audio.get_sample_size(format))
        sound_file.setframerate(frame_rate)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()

        # board.digital_write(YELLOW_LED, 0)
        # board.sleep(2)
        print("Done saving.")
        print("Processing FFT ...")
        samp_freq, sound = wavfile.read(wav_filename)
        sound = sound / 2.0 ** 15

        length_in_s = sound.shape[0] / samp_freq

        _time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

        signal = sound[:, 0]

        fft_spectrum = np.fft.rfft(signal)
        freq = np.fft.rfftfreq(signal.size, d=1. / samp_freq)
        fft_spectrum_abs = np.abs(fft_spectrum)

        fr = []
        for i, f in enumerate(fft_spectrum_abs):
            if f > 350:  # looking at amplitudes of the spikes higher than 350
                fr.append((np.round(freq[i], 1), np.round(f)))
                print('frequency = {} Hz with amplitude {} '.format(np.round(freq[i], 1), np.round(f)))

        for i, f in enumerate(freq):
            if f < 62 and f > 58:  # (1)
                fft_spectrum[i] = 0.0
            if f < 21 or f > 3000:  # (2)
                fft_spectrum[i] = 0.0

        do_fft(fft_spectrum)
        board.sleep(2)
        board.digital_write(YELLOW_LED, 0)
        print("Done.")

    if _play["led_state"] == 1:
        print(20 * '=')
        print("Opening '" + wav_filename + "' ...")
        board.sleep(2)
        # wav = AudioSegment.from_wav(wav_filename)
        # play(wav)

        for f in rec["frequencies"]:
            print(f)
            board.play_tone(BUZZER, Constants.TONE_TONE, int(f), 0)
            #board.sleep(.005)

        board.sleep(2)

        board.play_tone(BUZZER, Constants.TONE_NO_TONE, 0, 0)

        _play["led_state"] = 0
        board.digital_write(GREEN_LED, _play["led_state"])
        board.sleep(2)
        print("Finnished.")
        print(20 * '=')


############ USER FUNCTIONS ############
def do_fft(freq):
    #freq_interpolated = interp1d(freq, np.arange(1, 1023))

    for f in freq:
        rec["frequencies"].append(f)

    print(rec["frequencies"])

# ARDUINO RUN
if __name__ == "__main__":
    setup()
    while True:
        loop()