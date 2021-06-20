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
        t = organisms.Food_source(probOfPredator)
        trees.append(t)

    return evolvers, trees

def save(food_source):
    pass


def treeAction(trees, warner_survival_prob, prob_imposter_recognition):
    evolvers = []

    #note to self: to improve clarity could add warn and no_warn functions
    for t in trees:
        if t.isPredator:
            if len(t.eaters) > 1:
                randomizer = random.random()
                if t.eaters[1].allele == 'altruist':
                    evolvers.append(t.eaters[0])
                    if randomizer < warner_survival_prob: 
                        evolvers.append(t.eaters[1])
                elif t.eaters[1].allele == 'coward' or t.eaters[1].allele == 'imposter':
                    evolvers.append(t.eaters[1])
                elif t.eaters[1].allele == 'true_beard':
                    if t.eaters[0].allele == 'true_beard':
                        evolvers.append(t.eaters[0])
                        if randomizer < warner_survival_prob:
                            evolvers.append(t.eaters[1])
                    elif t.eaters[0].allele == 'imposter':
                        recognition_randomizer = random.random()
                        if recognition_randomizer < prob_imposter_recognition:
                            evolvers.append(t.eaters[1])
                        else:
                            evolvers.append(t.eaters[0])
                            if randomizer < warner_survival_prob:
                                evolvers.append(t.eaters[1])
                    else:
                        evolvers.append(t.eaters[1])

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
    freshData = dataOfAlive
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

    freshData['altruists'].append(n_of_altruists)
    freshData['cowards'].append(n_of_cowards)
    freshData['true_beards'].append(n_of_truebeards)
    freshData['imposters'].append(n_of_imposters)

    return freshData

def initial_count(evolvers):

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
        'altruists': [n_of_altruists],
        'cowards': [n_of_cowards],
        'true_beards': [n_of_truebeards],
        'imposters': [n_of_imposters]
    }

    return dataOfAlive


def simulationInstance(nOfDays, nOfEvolvers, nOfTrees, probOfPredator, warner_survival_rate, prob_imposter_recognition = 0):

    evolvers, trees = setUpOrganisms(nOfEvolvers, nOfTrees, probOfPredator)
    dataOfAlive = initial_count(evolvers)

    for d in range(nOfDays):

        #Attach each evolver to a randomly chosen tree
        random.shuffle(evolvers)
        for e in evolvers:
            indexOfTree = random.randint(0, len(trees) - 1)
            trees[indexOfTree].attachEvolver(e)

        #Eating at tree, dying if there is a predator etc.
        evolvers = treeAction(trees, warner_survival_rate, prob_imposter_recognition)

        #Breeding: returning a new list with each item from the original duplicated
        evolvers = breeding(evolvers)

        dataOfAlive = addDaysData(evolvers, dataOfAlive)

    return dataOfAlive

def average_of_instances(n_of_instances, n_of_days, n_of_evolvers, n_of_trees, prob_of_predator, warner_survival_rate, prob_imposter_recognition = 0):

    all_instances = simulationInstance(n_of_days, n_of_evolvers, n_of_trees, prob_of_predator, warner_survival_rate, prob_imposter_recognition)
    #converting all_instances values into lists of lists
    for allele in all_instances:
        index = 0
        for num in all_instances[allele]:
            all_instances[allele][index] = [all_instances[allele][index]]
            index += 1


    for i in range(n_of_instances - 1):
        merge_instance = simulationInstance(n_of_days, n_of_evolvers, n_of_trees, prob_of_predator, warner_survival_rate, prob_imposter_recognition)
        for allele in all_instances:
            index = 0
            for values in all_instances[allele]:
                values.append(merge_instance[allele][index])
                index += 1

    #turning back into a single array with averaged values
    for allele in all_instances:
        index = 0
        for values in all_instances[allele]:
            total = 0
            for value in values:
                total += value
            avg_value = total / len(values)
            all_instances[allele][index] = avg_value
            index += 1



    return all_instances

def plot_stackplot(data, x_values):
    # boring plotting stuff
    fig, ax = plt.subplots()
    ax.stackplot(x_values, data.values(),
                 labels=data.keys())
    ax.legend(loc='upper left')
    ax.set_title('Evolver populations')
    ax.set_xlabel('Day')
    ax.set_ylabel('Number of evolvers in system')

    plt.show()


def main():
    n_of_instances = 20
    n_of_days = 200
    n_of_evolvers = 200
    n_of_trees = 180
    prob_of_predator = 0.3
    warner_survival_rate = 0.5
    prob_imposter_recognition = 0

    populations = average_of_instances(n_of_instances, n_of_days, n_of_evolvers, n_of_trees, prob_of_predator, warner_survival_rate, prob_imposter_recognition)

    #creating an array of days for the x-axis of the plot
    days = [0]
    for i in range(n_of_days):
        days.append(i + 1)

    plot_stackplot(populations, days)

    test_values = []
    n_of_data_points = 10
    for i in range(n_of_data_points):
        test_values.append((i+1)/n_of_data_points)

    per_of_true_beards = []
    for recognition_prob in test_values:
        a_population = average_of_instances(n_of_instances, n_of_days, n_of_evolvers, n_of_trees, prob_of_predator,
                             warner_survival_rate, recognition_prob)
        n_of_green_beards = a_population["true_beards"][-1]
        total_of_evolvers = 0
        for allele in a_population:
            total_of_evolvers += a_population[allele][-1]
        per_of_true_beards.append(n_of_green_beards/total_of_evolvers)
        print(recognition_prob)

    plt.plot(test_values, per_of_true_beards)
    plt.xlabel('Probability of a Greenbeard Recognizing an Imposter')
    plt.ylabel('Ratio of Greenbeards to total population')
    plt.title(f'Propogation of the Greenbeard trait by the end of {n_of_days} day(s)')
    plt.show()



main()