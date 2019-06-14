import mido
from mido import MidiFile, MidiTrack, Message
import numpy as np
from random import randint
from random import uniform
import random

bach1 = MidiFile('training-songs/bach_846.mid')
bach2 = MidiFile('training-songs/bach_847.mid')
bach3 = MidiFile('training-songs/bach_850.mid')

file = MidiFile()


# testFile = MidiFile()
# testTrack = MidiTrack()
#
# for i, track in enumerate(bach1.tracks):
#     for msg in track:
#         if (not msg.is_meta) and msg.type == "note_on" and msg.channel == 0:
#             print(msg)
#             testTrack.append(msg)
# testFile.tracks.append(testTrack)

# testTrack = MidiTrack()
#
# for i, track in enumerate(bach1.tracks):
#     for msg in track:
#         if (not msg.is_meta) and msg.type == "note_on" and msg.channel == 3:
#             print(msg)
#             testTrack.append(msg)

# testFile.tracks.append(testTrack)
# testFile.save("Test.mid")


# TODO : IDEAS FOR IMPROVMENT
# 1. input more data (pieces) DONE ALSO SUCKS
# 2. transitions based on past TWO (note,time) pairs, not just the last one
# 3. could add multiple streams (i.e. whole hand playing)

##############################
#    Creates Markov Chain    #
##############################

def createChain(songs, channel):  # Takes in both a list of songs and a channel to base the chain off of
    DataList = makeDataList(songs, channel)

    size = len(DataList)
    print(size)
    tMatrix = np.zeros((size, size))

    prev = 0
    for song in songs:
        for i, track in enumerate(song.tracks):
            for msg in track:
                if msg.type == 'note_on' and msg.channel == channel:  ## REMOVED msg.time > 1
                    pair = (msg.note, msg.velocity, msg.time)
                    curr = DataList.index(pair)
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

def saveMidi(sequences, name):
    file = MidiFile()
    for sequence in sequences:
        result = MidiTrack()
        for (note, velocity, time) in sequence:
            result.append(mido.Message('note_on', note=note, velocity=velocity, time=time))
        file.tracks.append(result)

    file.save(name)


def makeDataList(songs, channel):
    notes = []
    velocities = []
    times = []

    result = []
    # Creates a list of all possible notes and times found in song
    for song in songs:
        for i, track in enumerate(song.tracks):
            for msg in track:
                if msg.type == 'note_on' and msg.channel == channel:
                    print(msg)
                    if (msg.note, msg.velocity, msg.time) not in result:
                        result.append((msg.note, msg.velocity, msg.time))
                    # if msg.time not in times:
                    #     times.append(msg.time)
                    # if msg.note not in notes:
                    #     notes.append(msg.note)
                    # if msg.velocity not in velocities:
                    #     velocities.append(msg.velocity)
    # notes.sort()
    # velocities.sort()
    # times.sort()
    # result = []
    # for i in range(len(notes)):
    #     for j in range(len(velocities)):
    #         for k in range(len(times)):
    #             if ()
    #             result.append((notes[i], velocities[j], times[k]))
    return result


def genSeq(chain, length, song, channel):
    seq = []
    DataList = makeDataList(song, channel)
    noteList = []
    velocityList = []
    timeList = []
    for (note, velocity, time) in DataList:
        if time not in timeList:
            timeList.append(time)
        if note not in noteList:
            noteList.append(note)
        if velocity not in velocityList:
            velocityList.append(velocity)

    while True:
        note = random.choice(noteList)
        velocity = random.choice(velocityList)
        time = random.choice(timeList)
        if (note, velocity, time) in DataList:
            break

    seq.append((note, velocity, time))

    for _ in range(length):
        sample = uniform(0, 1)
        if (note, velocity, time) not in DataList:
            while True:
                note = random.choice(noteList)
                velocity = random.choice(velocityList)
                time = random.choice(timeList)
                if (note, velocity, time) in DataList:
                    break

            seq.append((note, velocity, time))
        row = chain[DataList.index((note, velocity, time))]
        rowsum = 0
        for i in range(len(row)):
            if rowsum > sample:
                (note, velocity, time) = DataList[i]
                seq.append((note, velocity, time))
                break
            rowsum += row[i]
        if rowsum <= sample:
            note = random.choice(noteList)
            velocity = random.choice(velocityList)
            time = random.choice(timeList)
            seq.append((note, velocity, time))
    return seq


def matNorm(matrix):  # Mutates Matrix by Normalizing it
    for index in range(matrix.shape[0] - 1):
        if sum(matrix[index]) != 0:
            matrix[index] = matrix[index] / sum(matrix[index])


##############################
#          Running           #
##############################
def makeMidi(song):
    seqs = []
    for channel in [0, 2, 3, 4, 5]:
        chain = createChain(song, channel)
        seq = genSeq(chain, 200, song, channel)
        seqs.append(seq)

    saveMidi(seqs, "TrialThree.mid")


makeMidi([bach1, bach2])

# makeMidi(bach2, 0)


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
