import random,re

SEPARATOR = '~'
# This is for n>1 order Markov Chains:
splitter = re.compile("[^"+SEPARATOR+"]+")

# IF THIS ISN'T A "COMPLEX" PROJECT I DON'T KNOW WHAT IS

class MarkovChain():
    def __init__(self):
        self.matrix = {}
        self.lag = [] # For the starting returns

    def generateMatrix(self,data,order):
        '''
        There's a big problem in all of this!
        So, when we work out our probabilities, we look at our test data.
        The only problem is, the last few entries won't be looked at.
        So there will be a chance that the state will switch to one of those.
        Meaning that it won't have any idea what to do next.

        So, to deal with this, we'll instead have the data "loop":
        The data will have a few extra parts added to the end, so that these
        end transitions are added.
        '''
        self.o = order
        # First, the looping thing:
        for i in data:
            for j in range(self.o):
                if j < len(i):
                    i.append(i[j])
        # Find o-length sets and add the to a dictionary
        for i in data: # Presumes a dataset
            for j in range(len(i)-self.o):
                k = self.generateKey(i[j:j+self.o])
                n = i[j+self.o]
                if k in self.matrix.keys():
                    self.matrix[k].append(n)
                else:
                    self.matrix.update({k: [n]})
        # Randomly choose a start state:
        starts = []
        for i in data:
            starts.append(self.generateKey(i[0:self.o]))
        self.state = random.choice(starts)
        self.lag = self.getValues(self.state)

    def tick(self):
        if self.lag == []:
            available = self.matrix[self.state]
            newState = random.choice(available)
            self.state = self.updateKey(self.state,newState)
            return newState
        else:
            return self.lag.pop(0)

    def generateKey(self,vals):
        s = ''
        for i in vals:
            s += i + SEPARATOR
        return s[:-len(SEPARATOR)]

    def getValues(self,l):
        return splitter.findall(l)

    def updateKey(self,current,additional):
        # Remove the first one, update for additional, then get key
        t = self.getValues(current)
        t.append(additional)
        t.pop(0)
        return self.generateKey(t)
