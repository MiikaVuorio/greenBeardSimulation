import random

class Evolver:
#    eIterator = 0
    def __init__(self):
#        self.eID = Evolver.eIterator
#        Evolver.eIterator += 1
        self.feeding = False
        self.onTree = -1
        self.isAlive = True

    def kill(self):
        self.isAlive = False


class Tree:
#    tIterator = 0
    def __init__(self, probOfPredator):
        self.eaters = []
#       self.tID = Tree.tIterator
#        Tree.tIterator += 1
        if random.random() < probOfPredator:
            self.isPredator = True
        else:
            self.isPredator = False

    def attachEvolver(self, evolver):
        self.eaters.append(evolver)

    def eatersLeave(self):
        self.eaters = []