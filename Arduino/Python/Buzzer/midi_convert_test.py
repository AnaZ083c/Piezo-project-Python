from collections import defaultdict

import audio_to_midi
from pydub import AudioSegment
from pydub.playback import play
import os
import numpy as np
from scipy.io import wavfile

import matplotlib.pyplot as plt
import pretty_midi

file = "recording.wav"

wav = AudioSegment.from_wav(file)
# play(wav)

#os.system('audio-to-midi ./'+file+' -m -c -s -b 120')

midi_file = file+'.mid'
midi_data = pretty_midi.PrettyMIDI(midi_file)
# print('duration:', midi_data.get_end_time())
# print(f'{"note":>10} {"start":>10} {"end":>10}')
# for instrument in midi_data.instruments:
#     print("instrument:", instrument.program);
#     for note in instrument.notes:
#         print(f'{note.pitch:10} {note.start:10} {note.end:10}')

# fill with same start seconds
dict = defaultdict(list)

# get data from first instrument
for instrument in midi_data.instruments:
    for note in instrument.notes:
        start = int(note.start)
        dict[start].append(note.pitch)

print(dict)

# extract max note from each second
for key in dict.keys():
    tmp = dict[key]
    dict[key] = []
    dict[key].append(max(tmp))
    print(max(tmp))

print(dict)

dict2 = defaultdict(list)

for instrument in midi_data.instruments:
    for note in instrument.notes:
        start = int(note.start)
        dict2[start].append((note.pitch, note.start, note.end))

print(dict2)
for key in dict2.keys():
    first_pitch, first_start, first_end = dict2[key][0]
    last_pitch, last_start, last_end = dict2[key][len(dict2[key])-1]
    duration_s = last_end - first_start # duration in seconds
    note_hz = pretty_midi.note_number_to_hz(first_pitch)
    dict2[key] = (int(note_hz)-500, duration_s) # transpoze to piezo hz (max is cca 1800, more is questionable)

print(dict2)

dict3 = defaultdict(list)
for instrument in midi_data.instruments:
    for note in instrument.notes:
        start = int(note.start)
        duration_s = pretty_midi.Note.get_duration(note)
        dict3[start].append((note.pitch, duration_s))

print(dict3)
for key in dict3.keys():
    first_pitch, first_duration = dict3[key][0]
    last_pitch, last_duration = dict3[key][len(dict3[key])-1]
    duration_s = last_duration - first_duration # duration in seconds
    note_hz = pretty_midi.note_number_to_hz(first_pitch)
    dict3[key] = (int(note_hz)-500, duration_s) # transpoze to piezo hz (max is cca 1800, more is questionable)

print(dict3)