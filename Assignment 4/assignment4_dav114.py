import sys
sys.path.insert(0, './src')
import csv
import numpy as np
import scipy
import data_handler as dh
import learning as ln
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def main():
    #q4a()
    #q4b()
    q4c()
    
def q4a():
    # extract data
    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    PCA=0

    testError, trainError, cvError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=PCA, matrixList1=[2], matrixList2=[8])

    print "gamma: ", gamma, "\ttime: ", runTime, "\tC: ", C, "\tFeatures: ", PCA
    print "trainError: ", trainError[k], "\ttestError: ", testError[k], "\tcvError: ", cvError[k]

    graph_setup("gamma", "error", "Graph")
    graph_add(valErrors, "Train Error", 'red')
    plt.legend()
    plt.show()

def q4b():

    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    graph_setup("k", "Error", "graph")

    PCA = 1

    testError, trainError, cvError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=PCA, matrixList1=[2], matrixList2=[8])

    print "gamma: ", gamma, "\ttime: ", runTime, "\tC: ", C, "\tFeatures: ", k
    print "trainError: ", trainError, "\ntestError: ", testError, "\ncvError: ", cvError

    PCA_graph_add(trainError, "Train Error", 'blue')
    PCA_graph_add(testError, "Test Error", 'green')
    PCA_graph_add(cvError, "CV Error", 'red')

    plt.legend()
    plt.show()

def q4c():

    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    graph_setup("k", "Error", "graph")

    PCA = 2

    testError, trainError, cvError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=PCA, matrixList1=[1], matrixList2=[2,3,4,5,6,7,8,9])

    print "gamma: ", gamma, "\ttime: ", runTime, "\tC: ", C, "\tFeatures: ", k
    print "trainError: ", trainError, "\ntestError: ", testError, "\ncvError: ", cvError

    PCA_graph_add(trainError, "Train Error", 'blue')
    PCA_graph_add(testError, "Test Error", 'green')
    PCA_graph_add(cvError, "CV Error", 'red')

    plt.legend()
    plt.savefig("q3b.png")


def graph_setup(x, y, title):
    plt.figure()
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)

def PCA_graph_add(valErrors, PCA, color):
    data = {"color": [], "gamma": [], "y": [], "k": [], "C": []}
    for k, error in valErrors.items():
        data["k"].append(k)
        data["y"].append(error)

    plt.scatter(data["k"], data["y"], s=2, c=color, label = PCA);

def graph_add(valErrors, PCA, color):

    data = {"color": [], "gamma": [], "y": [], "k": [], "C": []}
    for k, gammaDict in valErrors.items():
        for (C, gamma), error in gammaDict.items():
            data["C"].append(C)
            data["k"].append(k)
            data["gamma"].append(gamma)
            data["y"].append(error)

    plt.scatter(data["gamma"], data["y"], s=2, c=color, label = PCA);



if __name__ == '__main__':
    main()
