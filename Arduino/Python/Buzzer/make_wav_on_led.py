from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import numpy as np
import pyaudio
import wave
import time
import audio_to_midi
import pretty_midi
from pydub import AudioSegment
from collections import defaultdict
import audio_to_midi
import os

from scipy.io import wavfile
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

    # REC ====led=on=button================
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

    # PLAY ===led=on=button================
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

    # DO REC
    if rec["led_state"] == 1:
        board.sleep(2)

        frame_rate = int(44100)
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
        print("Converting recording to MIDI...")

        os.system('audio-to-midi ./' + wav_filename + ' -m -c -s -b 120 -T -8') # convert .wav to MIDI, transpozing an octave down

        # get fequencies of the melody (kinda works)
        midi_file = wav_filename + '.mid'
        midi_data = pretty_midi.PrettyMIDI(midi_file)

        dict2 = defaultdict(list)

        for instrument in midi_data.instruments:
            for note in instrument.notes:
                start = int(note.start)
                if start != 0:
                    dict2[start].append((note.pitch, note.start, note.end))

        #print(dict2)
        for key in dict2.keys():
            first_pitch, first_start, first_end = dict2[key][0]
            last_pitch, last_start, last_end = dict2[key][len(dict2[key]) - 1]
            max_pitch = max([p for p, s, e in dict2[key]])
            duration_s = last_end - first_start  # duration in seconds
            note_hz = pretty_midi.note_number_to_hz(first_pitch)
            dict2[key] = (int(note_hz), duration_s)  # transpoze to piezo hz (max is cca 1800, more is questionable)

        # print out the freqs and their durations
        print("Frequencies are:")
        for key in dict2.keys():
            pitch_hz, duration_s = dict2[key]
            print(f"{key} => {pitch_hz}, {duration_s} \r")

        save_freqs_to_rec(dict2)

        board.sleep(2)
        board.digital_write(YELLOW_LED, 0)
        print("Done.")

    # DO PLAY
    if _play["led_state"] == 1:
        print(20 * '=')
        print("Opening '" + wav_filename + "' ...")
        board.sleep(2)
        # wav = AudioSegment.from_wav(wav_filename)
        # play(wav)

        for note_hz, duration_s in rec["frequencies"]:
            board.play_tone(BUZZER, Constants.TONE_TONE, note_hz, 0)
            board.sleep(duration_s)

        board.sleep(2)

        board.play_tone(BUZZER, Constants.TONE_NO_TONE, 0, 0)

        _play["led_state"] = 0
        board.digital_write(GREEN_LED, _play["led_state"])
        board.sleep(2)
        print("Finnished.")
        print(20 * '=')


############ USER FUNCTIONS ############
def save_freqs_to_rec(dict):
    rec["frequencies"] = []
    for key in dict:
        note_hz, duration_s = dict[key]
        rec["frequencies"].append((note_hz, duration_s))

    # print(rec["frequencies"])

# ARDUINO RUN
if __name__ == "__main__":
    setup()
    while True:
        loop()