from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import numpy as np
import keyboard
import pyaudio
import wave
import time


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
       "times_pressed": 0}

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

    # board.digital_write(RED_LED, rec["led_state"])
    # board.digital_write(GREEN_LED, _play["led_state"])

def loop():
    # board.digital_write(RED_LED, 0)
    # board.sleep(5)
    # board.digital_write(RED_LED, 1)
    # board.sleep(5)

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
        print("Done saving.")

    if _play["led_state"] == 1:
        print(20 * '=')
        print("Opening '" + wav_filename + "' ...")
        board.sleep(2)
        wav = AudioSegment.from_wav(wav_filename)
        play(wav)
        _play["led_state"] = 0
        board.digital_write(GREEN_LED, _play["led_state"])
        board.sleep(2)
        print("Finnished ...")
        print(20 * '=')


############ USER FUNCTIONS ############
def record_wav(filename, trigger):
    frame_rate = int(48000)
    frames_per_buff = int(1024)
    format = pyaudio.paInt16
    channels = 2

    audio = pyaudio.PyAudio()
    pyaudio.Stream.input_device_index = 2
    default_input_dev = audio.get_default_input_device_info()
    print(default_input_dev['index'], default_input_dev['name'], default_input_dev['maxInputChannels'])
    for i in range(audio.get_device_count()):  # list all available audio devices
        dev = audio.get_device_info_by_index(i)
        print((i, dev['name'], dev['maxInputChannels']))

    stream = audio.open(format=format, input_device_index=2, channels=channels, rate=frame_rate, input=True,
                        frames_per_buffer=frames_per_buff)

    frames = []

    while not bool(trigger):
        data = stream.read(frames_per_buff)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open(filename, 'wb')
    sound_file.setnchannels(channels)
    sound_file.setsampwidth(audio.get_sample_size(format))
    sound_file.setframerate(frame_rate)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

# ARDUINO RUN
if __name__ == "__main__":
    setup()
    while True:
        loop()