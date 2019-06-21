import mido
from mido import MidiFile, MidiTrack, Message
import numpy as np
from random import randint
from random import uniform
import random

##############################
#      GENERAL FRAMEWORK     #
##############################

def getP(songs, channel, hindsight): #Gives Transition Matrix based on songs, channel, and hindsight
    dataList = getDataList(songs, channel, hindsight)
    size = len(dataList)
    tMatrix = np.zeros((size, size))

    for song in songs:
        prev = ()
        for i, track in enumerate(song.tracks):
            for msg in track:
                if (msg.type == 'note_on' or msg.type == 'note_off') and msg.channel == channel:
                    curr = (msg.type == 'note_on', msg.note, msg.velocity, msg.time)

                    #Indices in matrix
                    curr_index = dataList.index(curr)
                    prev_index = dataList.index(prev)

                    tMatrix[prev_index][curr_index] = tMatrix[prev_index][curr_index] + 1

                    prev = prevAppend(prev, msg, hindsight) #Updates Previous

    matNorm(tMatrix)
    return tMatrix

def genSeq(length, songs, maxHindsight, channel):

    dataList = getDataList(songs, channel, maxHindsight)
    prev = genOriginal(songs, channel, maxHindsight)
    chain = getP(songs, channel, maxHindsight)
    result = []

    for _ in range(length):
        curr = sample(chain, prev, dataList)
        result.append(curr)
        prev = prevAppend(prev, curr, maxHindsight)


    return result

def getDataList(songs, channel, hindsight):
    result = []
    #tuples take format (TYPE, NOTE, VELOCITY, TIME) OR (prevHINDSIGHT..., prev3, prev2, prev1) where prev3 is the 3rd newest
    #Creates a list of all possible from's and to's in the songs
    for song in songs:
        prev = ()
        for i, track in enumerate(song.tracks):

            for msg in track:
                if (msg.type == 'note_on' or msg.type == 'note_off') and msg.channel == channel: #Note: Curr is current note, Prev is previous notes up to hindsight many
                    curr = (msg.type == 'note_on', msg.note, msg.velocity, msg.time)

                    if curr not in result:
                        result.append(curr)
                    if prev not in result:
                        result.append(prev)

                    prev = prevAppend(prev, msg, hindsight)

    return result

def makeMidi(songs, channel, hindsight):

    seq = genSeq(200, songs, hindsight, channel)
    saveMidi(seq, "NewCode.mid")



##############################
#       Helper Methods       #
##############################

def matNorm(matrix):  # Mutates Matrix by Normalizing it
    for index in range(matrix.shape[0] - 1):
        if sum(matrix[index]) != 0:
            matrix[index] = matrix[index] / sum(matrix[index])

def prevAppend(prev, msg, hindsight, tuple = None): #Appends new message to old previous tuple, and also cuts off first if needed to maintain len <= hindsight
    if type(msg) is tuple == False: #If message is passed in
        if len(prev) < hindsight:  # Insures prev does not have more than hindsight many previous notes
            prev = prev + ((msg.type == 'note_on', msg.note, msg.velocity, msg.time),)
            return prev
        else:
            temp = ()
            for i in range(1, len(prev)):
                temp = temp + (prev[i],)
            temp = temp + ((msg.type == 'note_on', msg.note, msg.velocity, msg.time),)
            return temp

    else: #If tuple is passed in
        if len(prev) < hindsight:
            prev = prev + (tuple,)
            return prev
        else:
            temp = ()
            for i in range(1, len(prev)):
                temp = temp + (prev[i],)
            temp = temp + (tuple,)
            return temp

def sample(pk, kTuple, dataList): #Returns the next note, if valid previous combination
    #pk = tMatrix, kTuple = previous notes, dataList = all possible combinations

    if kTuple not in dataList:
        return False

    sum = 0
    sample = uniform(0, 1)
    row = pk[dataList.index(kTuple)]
    for i in range(len(dataList)):
        sum += row[i]
        if sum >= sample:
            return dataList[i]

def getPrevs(songs, channel, hindsight): #Returns all possible prev states in the form of a list

    result = []
    for song in songs:
        prev = ()
        for i, track in enumerate(song.tracks):
            for msg in track:
                if (msg.type == 'note_on' or msg.type == 'note_off') and msg.channel == channel:
                    result.append(prev)
                    prev = prevAppend(prev, msg, hindsight) #Updates Previous

    return result

def genOriginal(songs, channel, hindsight):

    return random.choice(getPrevs(songs, channel, hindsight))

def saveMidi(sequence, name):
    file = MidiFile()
    result = MidiTrack()

    for (type, note, velocity, time) in sequence:
        if type == True:
            result.append(mido.Message('note_on', note=note, velocity=velocity, time=time))
        else:
            result.append(mido.Message('note_off', note=note, velocity=velocity, time=time))



    file.tracks.append(result)

    file.save(name)


##############################
#           Running          #
##############################

bach1 = MidiFile('training-songs/bach_846.mid')
bach2 = MidiFile('training-songs/bach_847.mid')
bach3 = MidiFile('training-songs/bach_850.mid')

file = MidiFile()

makeMidi([bach1], 0, 6)