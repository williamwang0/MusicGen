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


# TODO : IDEAS FOR IMPROVEMENT
# 1. input more data (pieces) DONE ALSO SUCKS
# 2. transitions based on past TWO (note,time) pairs, not just the last one DONE ? Maybe with some bugs
# 3. could add multiple streams (i.e. whole hand playing) DONE ALSO SUCKS

##############################
#    Creates Markov Chain    #
##############################

def createChain(songs, channel):  # Takes in both a list of songs and a channel to base the chain off of
    DataList = makeDataList(songs, channel)

    size = len(DataList)
    print(size)
    tMatrix = np.zeros((size, size))

    prev = 0
    prev_note = 0
    for song in songs:
        for i, track in enumerate(song.tracks):

            for msg in track:
                if msg.type == 'note_on' and msg.channel == channel:  ## REMOVED msg.time > 1
                    pair = (prev_note, msg.note, msg.velocity, msg.time)
                    if (prev_note, msg.note, msg.velocity, msg.time) == (72, 60, 61, 1):
                        print("should be in chain")
                    curr = DataList.index(pair)
                    if prev != 0:
                        tMatrix[prev][curr] += 1
                    prev = curr
                    prev_note = msg.note



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

    result = []
    # Creates a list of all possible notes and times found in song
    prev = 0
    for song in songs:
        for i, track in enumerate(song.tracks):

            for msg in track:
                if msg.type == 'note_on' and msg.channel == channel:
                    if (prev, msg.note, msg.velocity, msg.time) == (72, 60, 61, 1):
                        print("YES INCLUDED")
                    if (prev, msg.note, msg.velocity, msg.time) not in result:
                        result.append((prev, msg.note, msg.velocity, msg.time))

                    prev = msg.note

    return result


def genSeq(chain, length, song, channel):
    seq = []
    DataList = makeDataList(song, channel)
    noteList = []
    velocityList = []
    timeList = []

    for (prev, note, velocity, time) in DataList:
        if time not in timeList:
            timeList.append(time)
        if (prev, note) not in noteList:
            noteList.append((prev, note))
        if velocity not in velocityList:
            velocityList.append(velocity)

    while True: #Initializes first tuple combination in chain
        rand = random.choice(noteList)
        prev, note = rand[0], rand[1]
        velocity = random.choice(velocityList)
        time = random.choice(timeList)
        if (prev, note, velocity, time) in DataList: #Insures a valid combination
            break

    seq.append((note, velocity, time))

    for _ in range(length): #TRAVERSING CHAIN

        sample = uniform(0, 1) # Random Number Generated for Cumulative Sum
        if (prev, note, velocity, time) not in DataList:
            while True:
                rand = random.choice(noteList)
                prev, note = rand[0], rand[1]
                velocity = random.choice(velocityList)
                time = random.choice(timeList)
                if (note, velocity, time) in DataList:
                    break

            seq.append((note, velocity, time))


        row = chain[DataList.index((prev, note, velocity, time))]  #All possible transitions
        rowsum = 0

        for i in range(len(row)): #Cumulative Sum
            if rowsum > sample:
                (prev, note, velocity, time) = DataList[i]
                seq.append((note, velocity, time))
                break
            rowsum += row[i]
        if rowsum <= sample: #Edge Case? The rowsum is less than 1 due to rounding errors. i.e Sample is 1, but 3 possible outcomes w/probability 3.3333333
            #BUG HERE? NOTE VELOCITY TIME NOT IN DATALIST IS POSSIBLE
            """note = random.choice(noteList)
            velocity = random.choice(velocityList)
            time = random.choice(timeList)
            seq.append((note, velocity, time))"""
            if (prev, note, velocity, time) not in DataList:
                while True:
                    prev = random.choice(noteList)
                    note = random.choice(noteList)
                    velocity = random.choice(velocityList)
                    time = random.choice(timeList)
                    if (note, velocity, time) in DataList:
                        break

    return seq


def matNorm(matrix):  # Mutates Matrix by Normalizing it
    for index in range(matrix.shape[0] - 1):
        if sum(matrix[index]) != 0:
            matrix[index] = matrix[index] / sum(matrix[index])


##############################
#          Running           #
##############################
def makeMidi(song, channels):
    seqs = []
    for channel in channels:
        chain = createChain(song, channel)
        seq = genSeq(chain, 200, song, channel)
        seqs.append(seq)

    saveMidi(seqs, "TrialThree.mid")


makeMidi([bach1, bach2], [0,2,3,4,5])
