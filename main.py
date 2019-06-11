import mido
from mido import Message
from mido import MidiFile

bach1 = MidiFile('bach_846.mid')

for i, track in enumerate(bach1.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        print(msg)

