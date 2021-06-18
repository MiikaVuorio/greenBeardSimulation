import random

class Evolver:

    def __init__(self):
        self.fed = False
        self.onTree = -1
        self.isAlive = True

    def kill(self):
        self.isAlive = False


class Tree:

    def __init__(self, probOfPredator):
        self.eaters = []

        if random.random() < probOfPredator:
            self.isPredator = True
        else:
            self.isPredator = False

    def attachEvolver(self, evolver):
        self.eaters.append(evolver)

    def eatersLeave(self):
        self.eaters = []
