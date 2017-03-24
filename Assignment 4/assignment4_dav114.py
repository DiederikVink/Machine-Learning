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
    plt.savefig("q3a.png")

def q4b():

    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    graph_setup("k", "Error", "graph")

    PCA = 1

    rbf, trainSVMY, testSVMY, trainXIn, testXIn, trainY, testY, testError, trainError, cvError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=PCA, matrixList1=[2], matrixList2=[8])

    print "gamma: ", gamma, "\ttime: ", runTime, "\tC: ", C, "\tFeatures: ", k
    print "trainError: ", trainError, "\ntestError: ", testError, "\ncvError: ", cvError

    PCA_graph_add(trainError, "Train Error", 'blue')
    PCA_graph_add(testError, "Test Error", 'green')
    PCA_graph_add(cvError, "CV Error", 'red')

    plt.legend()
    plt.savefig("q3b.png")

def q4c():

    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    graph_setup("k", "Error", "graph")

    PCA = 2

    print "----------------pca-------------------"
    rbf, trainSVMY, testSVMY, trainX, testX, trainY, testY, testError, trainError, cvError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=PCA, matrixList1=[1], matrixList2=[0,2,3,4,5,6,7,8,9])

    print "gamma: ", gamma, "\ttime: ", runTime, "\tC: ", C, "\tFeatures: ", k
    print "trainError: ", trainError, "\ntestError: ", testError, "\ncvError: ", cvError

    PCA_graph_add(trainError, "Train Error", 'blue')
    PCA_graph_add(testError, "Test Error", 'green')
    PCA_graph_add(cvError, "CV Error", 'red')

    plt.legend()
    plt.savefig("q3c-pca.png")

    graph_setup("feature1", "feature2", "PCA-graph")
    q4c_graph(testX, testY, rbf, "pca-contour-test.png")
    graph_setup("feature1", "feature2", "PCA-graph")
    q4c_graph(trainX, trainY, rbf, "pca-contour-train.png", 1)


    #------------------------------------------------------------------------------
    #               NEXT SECTION
    #------------------------------------------------------------------------------


    trainMatrix = dh.read_data('./data/features.train')
    testMatrix = dh.read_data('./data/features.test')
    
    PCA = 0

    print "----------------feature-------------------"
    rbf, trainSVMY, testSVMY, trainX, testX, trainY, testY, testError, trainError, cvError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=PCA, matrixList1=[1], matrixList2=[0,2,3,4,5,6,7,8,9])

    print "gamma: ", gamma, "\ttime: ", runTime, "\tC: ", C, "\tFeatures: ", k
    print "trainError: ", trainError, "\ntestError: ", testError, "\ncvError: ", cvError

    PCA_graph_add(trainError, "Train Error", 'blue')
    PCA_graph_add(testError, "Test Error", 'green')
    PCA_graph_add(cvError, "CV Error", 'red')

    plt.legend()
    plt.savefig("q3c-feature.png")


    graph_setup("feature1", "feature2", "feature-graph")
    q4c_graph(testX, testY, rbf, "feature-contour-test.png")
    graph_setup("feature1", "feature2", "feature-graph")
    q4c_graph(trainX, trainY, rbf, "feature-contour-train.png", 1)


def q4c_graph(dataX, dataY, rbf, filename, train=0):
    x_min, x_max = dataX[:, 0].min() - 0.1, dataX[:, 0].max() + 0.1
    y_min, y_max = dataX[:, 1].min() - 0.1, dataX[:, 1].max() + 0.1
    cont1, cont2 = np.meshgrid(np.linspace(x_min, x_max, 1000), np.linspace(y_min, y_max, 1000))
    Z = rbf.predict(np.c_[cont1.ravel(), cont2.ravel()])
    Z = Z.reshape(cont1.shape)
    SV = rbf.support_

    testCol = ['red' if x == 1 else 'blue' for x in dataY]
    if train:
        for x in SV:
            testCol[x] = 'magenta'

    plt.scatter(dataX[:,0], dataX[:,1], color=testCol, s=1, cmap=plt.cm.coolwarm)
    plt.contour(cont1, cont2, Z, levels=[0])
    plt.savefig(filename)


def matrixExtraction(trainMatrix, testMatrix, matrixList1, matrixList2):

    twoMatrix, twoY = dh.extract_value(trainMatrix, matrixList1, -1)
    eightMatrix, eightY = dh.extract_value(trainMatrix, matrixList2, 1)
    
    # create X and Y vectors
    trainY = np.append(twoY, eightY, axis = 0)
    trainX = np.append(twoMatrix, eightMatrix, axis = 0)

    # extract 2 and 8
    twoMatrix, twoY = dh.extract_value(testMatrix, matrixList1, -1)
    eightMatrix, eightY = dh.extract_value(testMatrix, matrixList2, 1)
    
    testY = np.append(twoY, eightY, axis = 0)
    testX = np.append(twoMatrix, eightMatrix, axis = 0)

    return trainX, trainY, testX, testY, trainCol, testCol

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
