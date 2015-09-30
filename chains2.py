import random
SEPARATOR = "." # Our separator character for n > 1 order chains' keys

class MarkovChain: # gosh this version is much larger than the previous one!
    def __init__(self):
        self.matrix = []
        self.state = "0"
    
    def generateMatrix(self,data,order,startkey="0"):
        # Generate a transition matrix from some data!
        # Please do not have SEPARATOR in your data or startkey
        # And have an integer order, for goodness' sake!
        prev = [startkey for i in range(order)] # Nothing has happened so far
        prevkey = self.generateKey(prev)
        t = {prevkey: {}}
        data.append(startkey) # We want the last piece of data to be considered too!
        for dataset in data:
            for d in dataset:
                if not (prevkey in t.keys()): # If it doesn't exist, add it!
                    t[prevkey] = {}
                if not (str(d) in t[prevkey].keys()): # Same here!
                    t[prevkey][str(d)] = 1 # Initialise it
                else:
                    t[prevkey][str(d)] += 1 # Increase it!
                newprev = self.generatePrev(d,prev) # Shift everything back
                prevkey = self.generateKey(newprev) # Get a new key
                prev = newprev[:] # Go go go!
        # Now turn the occurences into probabilities!
        for k in t:
            tot = 0.0
            for m in t[k]:
                tot += t[k][m]
            for m in t[k]:
                t[k][m] /= tot
        self.matrix = t # Yay, we win.
        self.o = order
        self.history = [startkey for i in range(order)]
        self.start = startkey
        self.state = startkey

    def tick(self):
        current = self.generateKey(self.history)
        lowerVals = []
        keys = []
        rand = random.random()
        for i in self.matrix[current]: # grab probabilities
            lowerVals.append(self.matrix[current][i])
            keys.append(i)
        for i in range(len(lowerVals)-1,0,-1): # make them cumulative
            lowerVals[i] = reduce(lambda x,y: x+y, lowerVals[:i+1])
        for i in range(len(lowerVals)):
            if rand < lowerVals[i]:
                self.history = self.generatePrev(keys[i],self.history)
                if keys[i] == self.start: # It has returned to the start
                    # so the history has to be reset.
                    # Start states are special.
                    self.history = [self.start for j in range(self.o)]
                return keys[i]

    def generateKey(self,data):
        # Generates a key consisting of first.next.next.next.last
        # (where last is the last recorded previous value, and first the
        # first recorded)
        k = ""
        for i in reversed(data):
            k += str(i) + SEPARATOR
        return k[:-1]

    def generatePrev(self,d,prev):
        # Shift the previous values back (removing the last)
        # and add the most recent d on.
        n = [d]
        for i in prev:
            n.append(i)
        return n[:-1]

class WeightedMarkovChain(MarkovChain):
    def generateMatrix(self,data,globalStates,weightData,order,startkey='0'):
        # Generate a transition matrix from some data!
        # This time it integrates the weight class idea!
        # So we have a set of globalStates, which can be chosen at runtime
        # Each transition has an extra weight for each global state
        # Which acts as a multiplier to that transition's probability when it's active
        # This state can be changed with changeGlobalState(), or by changing the globalState variable
        prev = [startkey for i in range(order)] # Nothing has happened so far
        prevkey = self.generateKey(prev)
        t = {prevkey: {}}
        w = {i: {prevkey: {}} for i in globalStates}
        data.append(startkey) # We want the last piece of data to be considered too!
        for dataset in data:
            for q in range(len(dataset)):
                d = dataset[q]
                if not (prevkey in t.keys()): # If it doesn't exist, add it!
                    t[prevkey] = {}
                    for i in w.keys():
                        w[str(i)][prevkey] = {}
                if not (str(d) in t[prevkey].keys()): # Same here!
                    t[prevkey][str(d)] = 1 # Initialise it
                    for i in w.keys():
                        w[str(i)][prevkey][str(d)] = 1
                else:
                    t[prevkey][str(d)] += 1 # Increase it!
                # Add to the global state multiplier:
                for i in weightData[q]:
                    w[str(i)][prevkey][str(d)] += 1
                newprev = self.generatePrev(d,prev) # Shift everything back
                prevkey = self.generateKey(newprev) # Get a new key
                prev = newprev[:] # Go go go!
        # Now turn the occurences into probabilities!
        for k in t:
            tot = 0.0
            for m in t[k]:
                tot += t[k][m]
            for m in t[k]:
                t[k][m] /= tot
        self.matrix = t # Yay, we win.
        self.o = order
        self.history = [startkey for i in range(order)]
        self.start = startkey
        self.weightMatrix = w
        self.globalState = globalStates[0]
        self.state = startkey

    def tick(self):
        current = self.generateKey(self.history)
        lowerVals = []
        keys = []
        rand = random.random()
        for i in self.matrix[current]: # grab probabilities
            lowerVals.append(self.matrix[current][i]*self.weightMatrix[self.globalState][current][i])
            keys.append(i)
        # Make the lowerVals add up to 1:
        tot = 0
        for i in lowerVals:
            tot += i
        for i in lowerVals:
            i /= tot
        for i in range(len(lowerVals)-1,0,-1): # make them cumulative
            lowerVals[i] = reduce(lambda x,y: x+y, lowerVals[:i+1])
        for i in range(len(lowerVals)):
            if rand < lowerVals[i]:
                self.history = self.generatePrev(keys[i],self.history)
                if keys[i] == self.start: # It has returned to the start
                    # so the history has to be reset.
                    # Start states are special.
                    self.history = [self.start for j in range(self.o)]
                return keys[i]
