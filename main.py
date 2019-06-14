import mido
from mido import MidiFile, MidiTrack, Message
import numpy as np
from random import randint
from random import uniform
import random

bach1 = MidiFile('training-songs/bach_846.mid')
bach2 = MidiFile('training-songs/bach_847.mid')
bach3 = MidiFile('training-songs/bach_850.mid')

# for i, track in enumerate(bach1.tracks):
#     for msg in track:
#         print(msg)

file = MidiFile()

# TODO : IDEAS FOR IMPROVMENT
# 1. input more data (pieces)
# 2. transitions based on past TWO (note,time) pairs, not just the last one
# 3. could add multiple streams (i.e. whole hand playing)

##############################
#    Creates Markov Chain    #
##############################

def createChain(song, channel):  # Takes in both a song and a channel to base the chain off of
    NoteTimeList = makeNoteTimeList(song, channel)


    size = len(NoteTimeList)
    tMatrix = np.zeros((size, size))

    prev = 0
    for i, track in enumerate(song.tracks):
        for msg in track:
            if msg.type == 'note_on' and msg.channel == channel and msg.time > 1:
                pair = (msg.note, msg.time)
                curr = NoteTimeList.index(pair)
                if prev != 0:
                    tMatrix[prev][curr] += 1
                prev = curr

    # prev = 0
    # for i, track in enumerate(song.tracks):
    #     for msg in track:
    #         if msg.type == 'note_on' and msg.channel == channel:
    #
    #             curr = msg.note
    #             if prev != 0:
    #                 normalizationVec[prev - 1] = normalizationVec[prev - 1] + 1
    #                 tMatrix[prev - 1][curr - 1] = tMatrix[prev - 1][curr - 1] + 1
    #             prev = curr

    matNorm(tMatrix)

    return tMatrix


##############################
#       Save Midi File       #
##############################

def saveMidi(sequence, vel, name):
    file = MidiFile()
    result = MidiTrack()
    for (note, time) in sequence:
        result.append(mido.Message('note_on', note=note, velocity=vel, time=time))

    file.tracks.append(result)
    file.save(name)


def makeNoteTimeList(song, channel):
    times = []
    notes = []

    # Creates a list of all possible notes and times found in song
    for i, track in enumerate(song.tracks):
        for msg in track:
            if msg.type == 'note_on' and msg.channel == channel:
                if msg.time not in times and msg.time > 1:
                    times.append(msg.time)
                if msg.note not in notes:
                    notes.append(msg.note)
    times.sort()
    notes.sort()
    result = []
    for i in range(len(notes)):
        for j in range(len(times)):
            result.append((notes[i], times[j]))
    return result


def genSeq(chain, length, song, channel):
    seq = []
    NoteTimeList = makeNoteTimeList(song, channel)
    timeList = []
    noteList = []
    for (note, time) in NoteTimeList:
        if time not in timeList:
            timeList.append(time)
        if note not in noteList:
            noteList.append(note)


    while True:
        note = random.choice(noteList)
        time = random.choice(timeList)
        if (note, time) in NoteTimeList:
            break

    seq.append((note, time))

    for _ in range(length):
        sample = uniform(0, 1)
        row = chain[NoteTimeList.index((note, time))]
        rowsum = 0
        for i in range(len(row)):
            if rowsum > sample:
                (note, time) = NoteTimeList[i]
                seq.append((note, time))
                break
            rowsum += row[i]
        if rowsum <= sample:
            note = random.choice(noteList)
            time = random.choice(timeList)
            seq.append((note, time))
    return seq


def matNorm(matrix): #Mutates Matrix by Normalizing it
    for index in range(matrix.shape[0] - 1):
        if sum(matrix[index]) != 0:
            matrix[index] = matrix[index] / sum(matrix[index])


##############################
#          Running           #
##############################
def makeMidi(song, channel):
    chain = createChain(song, channel)
    seq = genSeq(chain, 200, song, channel)
    saveMidi(seq, 64, "TrialTwo.mid")

makeMidi(bach2, 0)



# chain = createChain(bach1, 2)
# count = 0
# for i in chain:
#     if sum(i) > 0:
#         count += 1
#     print(sum(i))
# #
# print(count)

# for i in range(len(chain)):
#     flag = True
#     for x in chain[i]:
#         if x:
#             flag = False
#             print(i)



# seq = genSeq(chain, 200)
# saveMidi(seq, 64, 100, "TrialOne.mid")

