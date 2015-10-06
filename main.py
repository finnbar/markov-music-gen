# EPQ: Generative Music
# musicbot3000!

'''
IDEAS FOR IMPROVEMENT:
* Sometimes it gets stuck on one note. Maybe try increasing the melody order?
  ACTUALLY I REALLY NEED TO JUST ADD MORE SOURCES, COME ON.
* It can't make minor music. Yet.
* Its music isn't great (MORE SOURCES ALREADY).
'''

KEY = "C" # The key of our output music
MELODY_ORDER = 2 # The order of the Markov Chain/Process for MELODY
RYTHMN_ORDER = 4 # The order of the Markov Chain/Process for RYTHMN
OUTPUT_LENGTH = 8 # Number of bars of output
TIME_SIGNATURE = 4.0 # Beats in a bar!
TINTINN = False
T_VOICE = 1 # Variation for the Tintinnabuli method (+ 1 2 3 ONLY)

from music21 import * # *feels the fury of the Python Gods*
from chains3 import *
import os,copy,re

spaceremover = re.compile("  ")

def getMelodyData(data):
    melodyData = []
    weightData = []
    for d in data:
        part = d.parts[0].getElementsByClass(stream.Measure) # Returns a list of Measures
        key = note.Note(part[0].keySignature.getScale().tonic)
        # Now, am I going to get "key" from keysignature or underlying chord?
        # Probably chord, so I need to rewrite the <key> stuff...
        melodyData.append([])
        for m in part: # For each measure!
            if(m.keySignature): key = note.Note(m.keySignature.getScale().tonic)
            for n in m.notesAndRests:
                if(type(n) == note.Note):
                    melodyData[-1].append(interval.Interval(key,n).simpleName)
                elif(type(n) == note.Rest):
                    melodyData.append([])
                else: # It's a chord! Get the top note!
                    melodyData[-1].append(interval.Interval(key,n[-1]).simpleName)
                if(n.offset == 0.0):
                    weightData.append(['f','f','f']) # extra copies of state => higher weighting
                elif(n.offset == m.barDuration.quarterLength - 1):
                    weightData.append(['l','l','l'])
                else:
                    weightData.append([])
    return (melodyData,weightData)

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

def createTitle():
    d = [[]]
    f = file("songnames.txt","r")
    data = f.readline()
    for i in data:
        if d==" ":
            d.append([])
        else:
            d[-1].append(i)
    T = MarkovChain()
    T.generateMatrix(d,2)
    n = ""
    for i in range(random.randrange(5,20)):
        n += str(T.tick())
    n = spaceremover.sub(" ",n)
    return n

def generateMusic():
    # Let's go!
    # First, we need to collect our data!
    # We look in /data to get our data.
    print "Hello!"
    data = []
    datadir = "data"
    for f in os.listdir(datadir):
        if f.endswith(".xml"):
            if f[0] != "_":
                data.append(f)
    print data
    for i in range(len(data)):
        data[i] = converter.parse(datadir+'/'+data[i])
    print "Data collected!"
    # Now, we need to do the transition matrix stuff!
    # This is done through analysis by music21 and then Markov stuff from chains2
    # First, the melody stuff:
    melodyData,weightData = getMelodyData(data)
    #MelodyChain = WeightedMarkovChain()
    #MelodyChain.generateMatrix(melodyData,['o','f','l'],weightData,MELODY_ORDER,"X")
    MelodyChain = MarkovChain()
    MelodyChain.generateMatrix(melodyData,MELODY_ORDER)
    print "Melody data analysed!"
    # Now, the rythmn stuff:
    # We're going to have another Markov chain looking at rythmn...
    rythmnData, rythmnKey = getRythmnData(data)
    RythmnChain = MarkovChain()
    RythmnChain.generateMatrix(rythmnData,RYTHMN_ORDER)
    rythmnKey.update({"X": []}) # Just so it doesn't panic when it gets an X
    print "Rythmn data analysed!"
    # Let's simulate it now!
    # This is done by creating a Stream and appending the results of the Markov Chains/Processes to it
    tune = stream.Part()
    tune.append(meter.TimeSignature(str(int(TIME_SIGNATURE))+'/4'))
    tune.append(key.Key(KEY))
    currentBeat = rythmnKey[RythmnChain.tick()]
    while tune.duration.quarterLength < OUTPUT_LENGTH * TIME_SIGNATURE:
        print str(tune.duration.quarterLength) + "/" + str(OUTPUT_LENGTH * TIME_SIGNATURE)
        n = note.Note(KEY) # Temporary pitch
        durat = 0
        slur = True
        while slur:
            slur = False
            while currentBeat == []:
                currentBeat = copy.copy(rythmnKey[RythmnChain.tick()])
                if currentBeat == []: # if it's still not there
                    print "End of phrase"
            durat += currentBeat[0]
            currentBeat.pop(0)
            while currentBeat == []:
                currentBeat = copy.copy(rythmnKey[RythmnChain.tick()])
                if currentBeat == []: # if it's still not there
                    print "End of phrase"
            if currentBeat[0] == '+':
                slur = True
                currentBeat.pop(0)
            if durat >= TIME_SIGNATURE: # Prevents notes from being too long
                durat = TIME_SIGNATURE
                slur = False
        n.duration.quarterLength = durat
        tune.append(n)
    print "Rythmn determined!"
    # Start by adding generic (no octave) pitches
    c = 0
    stillgoing = True
    for i in tune.notesAndRests:
        if stillgoing:
            c+=1
            if(i.offset == 0.0):
                MelodyChain.globalState = 'f'
            elif(i.offset >= TIME_SIGNATURE - 1.0):
                MelodyChain.globalState = 'l'
            else:
                MelodyChain.globalState = 'o'
            interv = MelodyChain.tick()
            while interv == "X":
                interv = MelodyChain.tick()
                stillgoing = False
            p = interval.Interval(interv).transposePitch(pitch.Pitch(KEY))
            i.pitch = p
    # Now smooth out the octaves:
    for i in range(1,c):
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
    if TINTINN:
        # Now, Tintinnabuli!
        tinn = stream.Part()
        tinn.append(meter.TimeSignature(str(int(TIME_SIGNATURE))+'/4'))
        tinn.append(key.Key(KEY))
        for i in tune.notesAndRests:
            # Our base pitches:
            pitches = [note.Note(KEY+"3"),interval.transposeNote(note.Note(KEY+"3"),'M3'),interval.transposeNote(note.Note(KEY+"2"),'p5')]
            localpitches = {}
            for j in range(len(pitches)):
                localpitches.update({str(interval.Interval(pitches[j],i).semitones): pitches[j]})
            c = T_VOICE-1
            n = localpitches[sorted(localpitches)[c]]
            while interval.Interval(n,i).semitones % 12 == 1:
                c+=1
                if c>2: c=0
                n = localpitches[sorted(localpitches)[c]]
            # Actually add note to tinn line now, and then you win.
            n.quarterLength = i.quarterLength
            tinn.append(n)
        print "Tintinnabuli bass added!"
    finalScore = stream.Score()
    titleOfSong = createTitle()
    finalScore.insert(metadata.Metadata())
    finalScore.metadata.title = titleOfSong
    finalScore.metadata.composer = 'musicbot3000'
    print "Generated title!"
    finalScore.insert(0,tune)
    if TINTINN: finalScore.insert(0,tinn)
    finalScore.show()

if __name__ == '__main__':
    rythmnData = []
    rythmnKey = {}
    # This is our menu, where you can change settings and then generate music.
    inp = ""
    while not (inp in ["q","Q"]):
        print
        print "MENU"
        print "____"
        print "t) Change the time signature"
        print "k) Change the tonic of the key"
        print "o) Change the output length"
        print "m) Change the order of the melody matrix"
        print "r) Change the order of the rythmn matrix"
        print "n) Add a Tintinnabuli bassline"
        print "v) Choose a T-Voice (only applies to Tintinnabuli basslines)"
        print "g) Generate the music!"
        print "q) QUIT"
        inp = raw_input("What would you like to do? (type the letter) ")
        if inp in ["t","T"]:
            TIME_SIGNATURE = int(raw_input("Enter the number of beats in a bar: "))
        elif inp in ["k","K"]:
            KEY = raw_input("Enter the key (e.g. C), making sure it has a capital letter: ")
            KEY = KEY.replace("b","-")
        elif inp in ["o","O"]:
            OUTPUT_LENGTH = int(raw_input("Enter the output length (in bars): "))
        elif inp in ["m","M"]:
            MELODY_ORDER = int(raw_input("Enter the melody matrix order (number): "))
        elif inp in ["r","R"]:
            RYTHMN_ORDER = int(raw_input("Enter the rythmn order (number): "))
        elif inp in ["v","V"]:
            T_VOICE = int(raw_input("Enter the T-Voice number (1,2,3): "))
        elif inp in ["g","G"]:
            generateMusic()
    print "Bye for now!"
