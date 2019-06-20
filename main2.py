import mido
from mido import MidiFile, MidiTrack, Message
import numpy as np
from random import randint
from random import uniform
import random

##############################
#      GENERAL FRAMEWORK     #
##############################

def getP(songs, hindsight):
    return

def genSeq(length, songs, maxHindsight):
    return

def Sample(pk, kTuple):
    return

def getDataList(songs, channel, hindsight):
    result = []
    prev = ()
    #tuples take format (TYPE, NOTE, VELOCITY, TIME) OR (..., prev3, prev2, prev1) where prev3 is the 3rd newest
    #Creates a list of all possible from's and to's in the songs
    for song in songs:
        for i, track in enumerate(song.tracks):

            for msg in track:
                if msg.type == 'note_on' or msg.type == 'note_off' and msg.channel == channel: #Note: Curr is current note, Prev is previous notes up to hindsight many
                    curr = (msg.type, msg.note, msg.velocity, msg.time)

                    if curr not in result:
                        result.append(curr)
                    if prev not in result:
                        result.append(prev)

                    if len(prev) < hindsight: #Insures prev does not have more than hindsight many previous notes
                        prev.append((msg.type, msg.note, msg.velocity, msg.time))
                    else:
                        temp = ()
                        for i in range(1, len(prev)):
                            temp.append(prev[i])
                        prev.append((msg.type, msg.note, msg.velocity, msg.time))

    return result