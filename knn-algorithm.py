import csv
import random
import math
import operator


def loadDataset(filename, trainingSet=[], testSet=[]):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if x < 40 or x > 59:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])

def loadDatasetRandom(filename, trainingSet=[], testSet=[]):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        for x in range(len(dataset) - 1):
            for y in range(4):
                dataset[x][y] = float(dataset[x][y])
            if random.random() < .2:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])



def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def classVote(neighbors):
    vote_for_1 = 0
    vote_for_2 = 0
    option_1 = 'Iris-versicolor'
    option_2 = 'Iris-virginica'
    for i in range(len(neighbors)):
        if (neighbors[i][4] == option_1):
            vote_for_1 = vote_for_1 + 1
        else:
            vote_for_2 = vote_for_2 + 1
    if (vote_for_1 > vote_for_2):
        return option_1
    else:
        return option_2


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(predictions)):
        if testSet[x][4] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0

def cross_validation():
    trainingSet = []
    testSet = []
    loadDatasetRandom('iris.data', trainingSet, testSet)
    predictions = []
    k = 5
    for i in range(1,5):
        for x in range(len(testSet)):
            neighbors = getNeighbors(trainingSet, testSet[x], k)
            result = classVote(neighbors)
            predictions.append(result)
            print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][4]))
        accuracy = getAccuracy(testSet, predictions)
        all_accuracies = []
        all_accuracies.append(accuracy)
    for i in range(len(all_accuracies)):
        accuracy_total = 0
        accuracy_total += all_accuracies[i]
    kfold_avg = accuracy_total / 5
    print("5 Fold Cross Validation of Iris Dataset =", kfold_avg,"%")



def main():
    # dataSet = input("What dataset would you like to run? \n").lower().strip()
    dataSet = 'iris'
    if dataSet == "iris":
        # prepare data
        trainingSet = []
        testSet = []
        # split = 0.2
        loadDataset('iris.data', trainingSet, testSet)
        print
        'Train set: ' + repr(len(trainingSet))
        print
        'Test set: ' + repr(len(testSet))
        # generate predictions
        predictions = []
        k = int(input("How many neighbors would you like to use this time? \n"))
        # for i in range(1, 10):
        #     if i % 2 != 0:
        #         k = i
        for x in range(len(testSet)):
            neighbors = getNeighbors(trainingSet, testSet[x], k)
            result = classVote(neighbors)
            predictions.append(result)
            print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][4]))
        accuracy = getAccuracy(testSet, predictions)
        print('Accuracy of k = ', k, ' : ' + repr(accuracy) + '%')


main()
#cross_validation()
# k = 9
#
# trainingSet = []
# testSet = []
# predictions = []
#
# loadDataset('iris.data', trainingSet, testSet)
# neighbors = getNeighbors(trainingSet, testSet[16], k)
#
# print(testSet[16][4])
# print(neighbors)
# #print(neighbors[0][4])
# result = classVote(neighbors)
# predictions.append(result)
# print(result)
# # print('> predicted=' + repr(result) + ', actual=' + repr(testSet[16][4]))
# accuracy = getAccuracy(testSet, predictions)
# print('Accuracy of k = ', k, ' : ' + repr(accuracy) + '%')


