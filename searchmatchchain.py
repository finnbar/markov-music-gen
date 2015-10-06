# Search/Match Markov Chain
# Rather than storing probabilities, a chain of data is stored and searched.
# This is similar to Kirsty's Regex Markov Chains!
# It's probably slower, although it is definitely less complex than my previous class.

import random

class MarkovChain(object):
    def __init__(self,data,order,startkey="X"):
        '''
        data is our data, as a list of lists. Or a string.
        order is the order of the chain.
        startkey is what entry should be used for the start or end of data
        '''
        if type(data) != type([]):
            self.data = [data]
            # Just to make sure! This is for sets of data with only one piece
        else:
            self.data = data
        # Now check to make sure everything is a table:
        for i in range(len(self.data)):
            if type(self.data[i]) == type(" "): # It's a string! Lets make it a list:
                t = []
                for j in self.data[i]:
                    t.append(j)
                self.data[i] = t[:]
        # Cool, now we've got a list of lists, let's append the start and end codes:
        for i in range(len(self.data)):
            for j in range(order):
                self.data[i].insert(0,startkey)
                self.data[i].append(startkey)
        self.o = order
        self.state = startkey
        self.history = [startkey for i in range(order)]

    def tick(self):
        res = []
        for i in self.data:
            for j in range(len(i)-self.o):
                # Let's search our table!
                found = True
                for k in range(self.o):
                    if i[j+k] != self.history[k]:
                        found = False
                        break
                if found:
                	# Weighting could be added here (with the transitions from The Music Instinct)
                    res.append(i[j+self.o])
        assert(res != [])
        self.state = random.choice(res)
        for i in range(len(self.history)-1):
            self.history[i] = self.history[i+1]
        self.history[-1] = self.state
        return self.state
