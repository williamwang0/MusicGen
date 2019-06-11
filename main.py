import mido
from mido import Message
from mido import MidiFile, MidiTrack

bach1 = MidiFile('bach_846.mid')

file = MidiFile()

for i, track in enumerate(bach1.tracks):
    print('Track {}: {}'.format(i, track.name))
    result = MidiTrack()

    for msg in track:
        print(msg)
        result.append(msg)

    file.tracks.append(result)

file.save("Testing.mid")