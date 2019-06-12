import mido
from mido import MidiFile, MidiTrack, Message
import numpy as np
from random import randint
from random import uniform

bach1 = MidiFile('bach_846.mid')

file = MidiFile()


##############################
#    Creates Markov Chain    #
##############################

def createChain(song, channel):  # Takes in both a song and a channel to base the chain off of
    tMatrix = np.zeros((127, 127))
    normalizationVec = np.zeros(127)

    prev = 0
    for i, track in enumerate(song.tracks):
        for msg in track:
            if msg.type == 'note_on' and msg.channel == channel:

                curr = msg.note
                if prev != 0:
                    normalizationVec[prev - 1] = normalizationVec[prev - 1] + 1
                    tMatrix[prev - 1][curr - 1] = tMatrix[prev - 1][curr - 1] + 1
                prev = curr

    for index in range(127):
        if normalizationVec[index] != 0:
            tMatrix[index] = tMatrix[index] / normalizationVec[index]

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


def genSeq(chain, length):
    lower, upper = 63, 83
    seq = []
    note = randint(lower, upper)
    seq.append(note)
    for _ in range(length):
        sample = uniform(0, 1)
        row = chain[note]
        rowsum = 0
        for i in range(len(row)):
            if rowsum > sample:
                note = i
                seq.append(note)
                break
            rowsum += row[i]
        if rowsum <= sample:
            note = randint(lower, upper)
            seq.append(note)
    return seq



##############################
#          Running           #
##############################


chain = createChain(bach1, 2)
for i in chain:
    print(i)


# for i in range(len(chain)):
#     flag = True
#     for x in chain[i]:
#         if x:
#             flag = False
#             print(i)

seq = genSeq(chain, 200)
saveMidi(seq, 64, 100, "TrialOne.mid")


file.save("Testing.mid")
