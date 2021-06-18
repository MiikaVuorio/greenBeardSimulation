import math
import numpy as np
import random
import matplotlib.pyplot as plt
import organisms


def setUpOrganisms(nOfEvolvers, nOfTrees, probOfPredator):

    #set up evolvers
    evolvers = []

    for i in range(nOfEvolvers):
        e = organisms.Evolver()
        evolvers.append(e)

    #set up trees
    trees = []

    for i in range(nOfTrees):
        t = organisms.Tree(probOfPredator)
        trees.append(t)

    return evolvers, trees


def treeAction(trees, warner_survival_prob):
    evolvers = []

    for t in trees:
        if t.isPredator:
            if len(t.eaters) > 1:
                randomizer = random.random()
                if t.eaters[0] == 'altruist':
                    evolvers.append(t.eaters[1])
                    if randomizer < warner_survival_prob:
                        evolvers.append(t.eaters[0])
                elif t.eaters[0] == 'coward' or t.eaters == 'imposter':
                    evolvers.append(t.eaters[0])
                elif t.eaters[0] == 'true_beard':
                    if t.eaters[1] == 'true_beard' or t.eaters[1] == 'imposter':
                        evolvers.append(t.eaters[1])
                        if randomizer < warner_survival_prob:
                            evolvers.append(t.eaters[0])

        else:
            eIndex = 0
            for e in t.eaters:
                if eIndex < 1:
                    evolvers.append(e)
                    eIndex += 1
        t.eatersLeave()

    return evolvers

def breeding(evolvers):
    afterMultEvolvers = []
    for e in evolvers:
        afterMultEvolvers.append(e)
        afterMultEvolvers.append(e)

    return afterMultEvolvers

def addDaysData(evolvers, dataOfAlive):
    n_of_altruists = 0
    n_of_cowards = 0
    n_of_truebeards = 0
    n_of_imposters = 0

    for e in evolvers:
        if e.allele == 'altrusit':
            n_of_altruists += 1
        elif e.allele == 'coward':
            n_of_cowards += 1
        elif e.allele == 'true_beard':
            n_of_truebeards += 1
        elif e.allele == 'imposter':
            n_of_imposters += 1

    dataOfAlive['altruits'].append(n_of_altruists)
    dataOfAlive['cowards'].append(n_of_cowards)
    dataOfAlive['true_beards'].append(n_of_truebeards)
    dataOfAlive['imposters'].append(n_of_imposters)

def initialCount(evolvers):
    n_of_altruists = 0
    n_of_cowards = 0
    n_of_truebeards = 0
    n_of_imposters = 0

    for e in evolvers:
        if e.allele == 'altruist':
            n_of_altruists += 1
        elif e.allele == 'coward':
            n_of_cowards += 1
        elif e.allele == 'true_beard':
            n_of_truebeards += 1
        elif e.allele == 'imposter':
            n_of_imposters += 1

    dataOfAlive = {
        'altruits': [n_of_altruists],
        'cowards': [n_of_cowards],
        'true_beards': [n_of_truebeards],
        'imposters': [n_of_imposters]
    }

    return dataOfAlive


def simulationInstance(nOfDays, nOfEvolvers, nOfTrees, probOfPredator, warner_survival_rate):

    evolvers, trees = setUpOrganisms(nOfEvolvers, nOfTrees, probOfPredator)
    dataOfAlive = initialCount(evolvers)
    print(dataOfAlive)

    for d in range(nOfDays):

        #Attach each evolver to a randomly chosen tree
        for e in evolvers:
            indexOfTree = random.randint(0, len(trees) - 1)
            trees[indexOfTree].attachEvolver(e)

        #Eating at tree, dying if there is a predator etc.
        evolvers = treeAction(trees, warner_survival_rate)

        #Breeding: returning a new list with each item from the original duplicated
        evolvers = breeding(evolvers)

        addDaysData(evolvers, dataOfAlive)

    return dataOfAlive

def main():
    nOfDays = 100
    nOfEvolvers = 500
    nOfTrees = 450
    probOfPredator = 0.25
    warner_survival_rate = 0.5

    populations = simulationInstance(nOfDays, nOfEvolvers, nOfTrees, probOfPredator, warner_survival_rate)

    days = [0]
    for i in range(nOfDays):
        days.append(i + 1)

    #boring plotting stuff
    fig, ax = plt.subplots()
    ax.stackplot(days, populations.values(),
                 labels=populations.keys())
    ax.legend(loc='upper left')
    ax.set_title('Evolver populations')
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of evolvers in system')

    plt.show()

main()