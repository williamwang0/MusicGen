import mido
from mido import MidiFile, MidiTrack, Message

def printMidi(songs):
    for msg in songs:
        print(msg)


sample = MidiFile('NewCode.mid')
printMidi(sample)