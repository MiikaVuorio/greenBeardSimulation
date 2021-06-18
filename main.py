import math
import numpy as np
import random
import matplotlib
import organisms

evolvers = []
trees = []
dataOfAlive = []
nOfDays = 9
nOfEvolvers = 100
nOfTrees = 100
probOfPredator = 0

for i in range(nOfEvolvers):
    e = organisms.Evolver()
    evolvers.append(e)
dataOfAlive.append(len(evolvers))

for i in range(nOfTrees):
    t = organisms.Tree(probOfPredator)
    trees.append(t)

for d in range(nOfDays):

    #Attach each evolver to a randomly chosen tree
    # lives = []
    for e in evolvers:
        indexOfTree = random.randint(0, len(trees) - 1)
        trees[indexOfTree].attachEvolver(e)
    #     lives.append(e.isAlive)
    # print(lives)

    #Tree action
    killed = 0
    nonPredCounts = 0
    for t in trees:
#        lives = []
#        for e in t.eaters:
#           lives.append(e.isAlive)
#       print(lives)
#         if t.isPredator:
#             for e in t.eaters:
#                 e.kill()
#         else:
#             indexOfEater = 0
#             for e in t.eaters:
#                 if indexOfEater > 1:
#                     killed += 1
#                     e.kill()
#                 #print(indexOfEater)
#                 indexOfEater += 1
#         t.eatersLeave()
        if len(t.eaters) > 1:
            for i in range(len(t.eaters) - 1):
                evolvers.pop(0)
        t.eatersLeave()

    #Clean evolvers list
    stillAliveEvolvers = []
    nOfAlive = 0
    for e in evolvers:
        #print(e.isAlive)
        if e.isAlive:
            stillAliveEvolvers.append(e)
            nOfAlive += 1
    #print(nOfAlive)
    evolvers = stillAliveEvolvers
    #print(len(evolvers))
    #following line for debug
    #print(f"pre-breeding: {len(evolvers)}")

    #Breeding
    afterMultEvolvers = []
    for e in evolvers:
        afterMultEvolvers.append(e)
        afterMultEvolvers.append(e)
    evolvers = afterMultEvolvers

    #following line for debug
    #print(f"post-breeding: {len(evolvers)}")
    dataOfAlive.append(len(evolvers))

print(dataOfAlive)
