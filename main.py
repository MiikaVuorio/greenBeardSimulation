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


def treeAction(trees):
    evolvers = []

    for t in trees:
        if t.isPredator:
            continue
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


def simulationInstance(nOfDays, nOfEvolvers, nOfTrees, probOfPredator):

    dataOfAlive = []
    evolvers, trees = setUpOrganisms(nOfEvolvers, nOfTrees, probOfPredator)

    dataOfAlive.append(len(evolvers))

    for d in range(nOfDays):

        #Attach each evolver to a randomly chosen tree
        for e in evolvers:
            indexOfTree = random.randint(0, len(trees) - 1)
            trees[indexOfTree].attachEvolver(e)

        #Eating at tree, dying if there is a predator etc.
        evolvers = treeAction(trees)

        #Breeding: returning a new list with each item from the original duplicated
        evolvers = breeding(evolvers)


        dataOfAlive.append(len(evolvers))

    return dataOfAlive

def main():
    nOfDays = 200
    nOfEvolvers = 100
    nOfTrees = 100
    probOfPredator = 0.2

    data = simulationInstance(nOfDays, nOfEvolvers, nOfTrees, probOfPredator)

    days = [0]
    for i in range(nOfDays):
        days.append(i + 1)

    #boring plotting stuff

    #keying (turning raw array data into dictionary form)
    populations = {
        'suckers': data
    }

    #making the actual plot
    fig, ax = plt.subplots()
    ax.stackplot(days, populations.values(),
                 labels=populations.keys())
    ax.legend(loc='upper left')
    ax.set_title('Evolver populations')
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of evolvers in system')

    plt.show()

main()