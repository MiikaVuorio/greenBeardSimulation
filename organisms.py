import random

class Evolver:

    def __init__(self, allele='init'):
        if allele == 'init':
            type_randomiser = random.random()
            if type_randomiser < 0.25:
                self.allele = 'sucker'
            elif type_randomiser < 0.5:
                self.allele = 'coward'
            elif type_randomiser < 0.75:
                self.allele = 'true_beard'
            else:
                self.allele = 'imposter'
        else:
            self.allele = allele

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
