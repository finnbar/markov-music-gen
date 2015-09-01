KEY = "C"
ORDER = 2
OUTPUT_LENGTH = 8

'''
This is the same way that MAG does it.
I don't really like it, it sounds too similar to the inputs.
When I have more sources, I might try it again, but for now this is second best.
'''

from music21 import *
from chains2 import *
import os,copy

def getChainData(data):
    chainData = []
    rythmnKey = {'a': 1.0}
    currentLetter = 'b'
    for d in data:
        part = d.parts[0].getElementsByClass(stream.Measure)
        key = part[0].keySignature.getScale().tonic
        chainData.append([])
        for m in part: # For each measure!
            if(m.keySignature): key = m.keySignature.getScale().tonic
            for n in m.notesAndRests:
                v = "R"
                if(type(n) == note.Note):
                    v = str(interval.notesToChromatic(key,n).mod12)
                    if not (n.quarterLength in rythmnKey.values()):
                        rythmnKey.update({currentLetter: n.quarterLength})
                        currentLetter = chr(ord(currentLetter)+1)
                    r = rythmnKey.keys()[rythmnKey.values().index(n.quarterLength)]
                else:
                    if not (n.duration.quarterLength in rythmnKey.values()):
                        rythmnKey.update({currentLetter: n.duration.quarterLength})
                        currentLetter = chr(ord(currentLetter)+1)
                    r = rythmnKey.keys()[rythmnKey.values().index(n.duration.quarterLength)]
                chainData[-1].append(v+r)
    return (chainData,rythmnKey)
                                     
if __name__ == '__main__':
    # Let's go!
    # First, we need to collect our data!
    # We look in /data to get our data.
    print "Hello!"
    data = []
    for f in os.listdir("data"):
        if f.endswith(".xml"):
            data.append(f)
    print data
    for i in range(len(data)):
        data[i] = converter.parse('data/'+data[i])
    print "Data collected!"
    # Now, both the melody and rythmn data:
    chainData,rythmnKey = getChainData(data)
    Chain = MarkovChain()
    Chain.generateMatrix(chainData,ORDER,"Ra")
    # Cool, let's make some music!
    tune = stream.Stream()
    while tune.duration.quarterLength < OUTPUT_LENGTH * 4:
        d = Chain.tick()
        n = note.Note(KEY)
        pit = d[:-1]
        ryt = rythmnKey[d[-1]]
        if pit == "R":
            n = note.Rest()
            n.duration.quarterLength = ryt
        else:
            p = interval.ChromaticInterval(int(pit)).transposePitch(pitch.Pitch(KEY))
            n.pitch = p
            n.quarterLength = ryt
        tune.append(n)
    # Octave smoothing
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
