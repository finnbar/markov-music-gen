from chains3 import *

# OK, let's write a song title! :D
# How are we doing that?
# We're going to use Markov Chains, as per usual :P

if __name__ == '__main__':
    generateTitle()

def generateTitle():
    numberOfTitles = 1
    chainOrder = 4
    trainingData = [] # This is the data from the song titles we're analysing.
    f = file("songnames.txt","r")
    data = f.readline()
    while data: # Essentially for each song title
        trainingData.append([])
        for i in data:
            trainingData[-1].append(i) # Append each letter
        data = f.readline()
    TitleGenerator = MarkovChain()
    TitleGenerator.generateMatrix(trainingData,chainOrder)
    currentTitle = ""
    while numberOfTitles > 0:
        nextCharacter = TitleGenerator.tick()
        if nextCharacter != "\n":
            currentTitle += nextCharacter
        else:
            return currentTitle
            currentTitle = ""
            numberOfTitles -= 1
