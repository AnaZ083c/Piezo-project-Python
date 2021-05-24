import pretty_midi
from pydub import AudioSegment
from collections import defaultdict
import audio_to_midi
import os

file = "rec32.wav"

os.system('audio-to-midi ./'+file+' -m -c -s -b 120 -T -8')
midi_file = file+'.mid'
midi_data = pretty_midi.PrettyMIDI(midi_file)

dict2 = defaultdict(list)

for instrument in midi_data.instruments:
    for note in instrument.notes:
        start = int(note.start)
        if start != 0:
            dict2[start].append((note.pitch, note.start, note.end))

print(dict2)
for key in dict2.keys():
    first_pitch, first_start, first_end = dict2[key][0]
    last_pitch, last_start, last_end = dict2[key][len(dict2[key])-1]
    duration_s = last_end - first_start # duration in seconds
    note_hz = pretty_midi.note_number_to_hz(first_pitch)
    dict2[key] = (int(note_hz), duration_s) # transpoze to piezo hz (max is cca 1800, more is questionable)

for key in dict2.keys():
    pitch_hz, duration_s = dict2[key]
    print(f"{key} => {pitch_hz}, {duration_s} \r")
