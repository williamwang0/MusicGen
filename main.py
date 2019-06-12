import mido
from mido import Message
from mido import MidiFile, MidiTrack
import numpy as np

bach1 = MidiFile('bach_846.mid')

file = MidiFile()

##############################
#    Creates Markov Chain    #
##############################

def createChain(song, channel): #Takes in both a song and a channel to base the chain off of
    tMatrix = np.zeros((100,100))
    normalizationVec = np.zeros(100)


    prev = 0
    for i, track in enumerate(bach1.tracks):
        for msg in track:
            if msg.type == 'note_on' and msg.channel == channel:

                curr = msg.note
                if prev != 0:
                    normalizationVec[prev-1] = normalizationVec[prev-1] + 1
                    tMatrix[prev-1][curr-1] = tMatrix[prev-1][curr-1] + 1
                prev = curr


    for index in range(100):
        if normalizationVec[index] != 0:
            tMatrix[index] = tMatrix[index] / normalizationVec[i]

    return tMatrix




##############################
#       Save Midi File       #
##############################

def saveMidi(sequence, vel, time, name):
    file = MidiFile()
    result = MidiTrack()

    for num in sequence:
        result.append(mido.Message('note_on', note=num, velocity=vel, time=time))

    file.tracks.append(result)
    file.save(name)


##############################
#          Running           #
##############################


chain = createChain(bach1, 2)
for i in chain:
    print(i)





"""for i, track in enumerate(bach1.tracks):
    print('Track {}: {}'.format(i, track.name))
    file.tracks.append(result)"""