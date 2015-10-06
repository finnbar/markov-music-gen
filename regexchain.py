# Regex Markov Chain
# Using regexes for Markov Chains
# I got this idea from Kirsty, and it's a brilliant one.

import random,re

class MarkovChain(object):
    # It's a new style class, ooh

    def __init__(self):
        self.data = ""
        self.state = "0"

    def setup(self,data,order,itemlength,startkey=""):
        '''
        This sets up our Markov Chain. We need to specify the data,
        the order of the Chain, how long each 
        '''
        if startkey == "":
            startkey = "X"*itemlength
        for i in data:
            self.data += (startkey*order) + i
        self.data += (startkey*order)
        self.o = order
        self.state = startkey
        self.history = (startkey*order)
        self.l = itemlength

    def tick(self):
        m = re.compile(self.history+"("+("."*self.l)+")")
        res = m.findall(self.data)
        print self.history,res
        # BUG: when a match is found, the char is removed, sometimes
        # meaning that other matches just don't appear.
        self.state = random.choice(res)
        self.history = self.history[self.l:] + self.state
        return self.state
