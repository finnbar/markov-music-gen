# EPQ: Generative Music
# Markov Music Generator (MMG) [needs better name]

KEY = "C" # The key of our output music
MELODY_ORDER = 2 # The order of the Markov Chain/Process for MELODY
RYTHMN_ORDER = 4 # The order of the Markov Chain/Process for RYTHMN
OUTPUT_LENGTH = 4 # Number of 4/4 bars of output

from music21 import * # *feels the fury of the Python Gods*
from chains2 import *
import os,copy

def getMelodyData(data):
    for d in data:
        part = d.parts[0].getElementsByClass(stream.Measure) # Returns a list of Measures
        key = part[0].keySignature.getScale().tonic
        # Now, am I going to get "key" from keysignature or underlying chord?
        # Probably chord, so I need to rewrite the <key> stuff...
        melodyData.append([])
        for m in part: # For each measure!
            if(m.keySignature): key = m.keySignature.getScale().tonic
            for n in m.notesAndRests:
                if(type(n) == note.Note):
                    melodyData[-1].append(interval.notesToChromatic(key,n).mod12)
                elif(type(n) == note.Rest):
                    melodyData.append([])
    return melodyData

def getRythmnData(data):
    currentLetter = 'a'
    for d in data: # I might add this loop to the previous loop for computation speed
        rythmnData.append([])
        part = d.parts[0].getElementsByClass(stream.Measure)
        overflow = 0 # how far we're into a single beat
        currentBeat = []
        for m in part:
            for n in m.notesAndRests:
                l = n.quarterLength
                while 1.0 - overflow - l < 0: # For notes longer than 1 beat
                    currentBeat.append(1.0 - overflow) # Fill the rest of the bar
                    currentBeat.append("+") # Show that it's tied over
                    # Add it to the rythmnData with the correct key
                    if currentBeat in rythmnKey.values():
                        rythmnData[-1].append(rythmnKey.keys()[rythmnKey.values().index(currentBeat)])
                    else:
                        rythmnKey.update({currentLetter: copy.copy(currentBeat)})
                        rythmnData[-1].append(currentLetter)
                        currentLetter = chr(ord(currentLetter)+1)
                    currentBeat = []
                    l -= 1 - overflow
                    overflow = 0
                if l > 0: # If, after truncating extra long notes, there's still some note left
                    currentBeat.append(l) # Finally, add the rest of the note, or the entire note if it was short
                    overflow += l
                if overflow == 1: # If that completes a beat (so should be added)
                    if currentBeat in rythmnKey.values():
                        rythmnData[-1].append(rythmnKey.keys()[rythmnKey.values().index(currentBeat)])
                    else:
                        rythmnKey.update({currentLetter: copy.copy(currentBeat)})
                        rythmnData[-1].append(currentLetter)
                        currentLetter = chr(ord(currentLetter)+1)
                    currentBeat = []
                    overflow = 0
    return (rythmnData,rythmnKey)

if __name__ == '__main__':
    # Let's go!
    # First, we need to collect our data!
    # We look in /data to get our data.
    print "Hello!"
    data = []
    for f in os.listdir("data"):
        if f.endswith(".xml"):
            data.append(f)
    for i in range(len(data)):
        data[i] = converter.parse('data/'+data[i])
    print "Data collected!"
    # Now, we need to do the transition matrix stuff!
    # This is done through analysis by music21 and then Markov stuff from chains2
    # First, the melody stuff:
    melodyData = [] # No idea why it has to be predefined...
    melodyData = getMelodyData(data)
    MelodyChain = MarkovChain()
    MelodyChain.generateMatrix(melodyData,MELODY_ORDER,"X")
    print "Melody data analysed!"
    # Now, the rythmn stuff:
    # We're going to have another Markov chain looking at rythmn...
    rythmnData = []
    rythmnKey = {}
    rythmnData, rythmnKey = getRythmnData(data)
    RythmnChain = MarkovChain()
    RythmnChain.generateMatrix(rythmnData,RYTHMN_ORDER,"X")
    rythmnKey.update({"X": []}) # Just so it doesn't panic when it gets an X
    print "Rythmn data analysed!"
    print rythmnKey
    # Let's simulate it now!
    # This is done by creating a Stream and appending the results of the Markov Chains/Processes to it
    tune = stream.Stream()
    currentBeat = rythmnKey[RythmnChain.tick()]
    while tune.duration.quarterLength < OUTPUT_LENGTH * 4:
        print str(tune.duration.quarterLength) + "/" + str(OUTPUT_LENGTH * 4)
        n = note.Note(KEY) # Temporary pitch
        durat = 0
        slur = True
        while slur:
            slur = False
            while currentBeat == []:
                currentBeat = copy.copy(rythmnKey[RythmnChain.tick()])
            durat += currentBeat[0]
            currentBeat.pop(0)
            while currentBeat == []:
                currentBeat = copy.copy(rythmnKey[RythmnChain.tick()])
            if currentBeat[0] == '+':
                slur = True
                currentBeat.pop(0)
        n.duration.quarterLength = durat
        tune.append(n)
    print "Rythmn determined!"
    # Start by adding generic (no octave) pitches
    for i in tune.notesAndRests:
        interv = MelodyChain.tick()
        while interv == "X":
            interv = MelodyChain.tick()
        p = interval.ChromaticInterval(int(interv)).transposePitch(pitch.Pitch(KEY))
        i.pitch = p
    # Now smooth out the octaves:
    for i in range(1,len(tune.notesAndRests)):
        e = tune.notesAndRests[i].pitch
        pe = tune.notesAndRests[i-1].pitch
        d = 10000 # difference
        correct = 3
        if e.octave:
            correct = e.octave - 1
        else:
            e.octave = correct
        e.octave = e.octave - 1 # Temporary...
        for j in range(3):
            e.octave += 1
            if d > abs(interval.notesToChromatic(pe,e).semitones):
                d = abs(interval.notesToChromatic(pe,e).semitones)
                correct = e.octave
        tune.notesAndRests[i].pitch.octave = correct
    print "Melody determined!"
    tune.show()
