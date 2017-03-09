import sys
sys.path.insert(0, './src/')
import time
import numpy as np
import data_handler as dh
import testing
import learning as lr
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.nan)


def main():
    trainData = dh.read_data('./movie-data/ratings-train.csv')
    testData = dh.read_data('./movie-data/ratings-test.csv')
    movFeat = dh.read_data('./movie-data/movie-features.csv')

    #q3a(trainData, testData)
    #q3b(movFeat, trainData, testData)    
    #q3c(movFeat, trainData, testData)
    q3d(movFeat, trainData, testData)


def q3a(trainData,testData):

    trainMovie = dh.sort(trainData, 1)
    meanMovie = dh.average(trainMovie, 1, 2, 9066)
    testMovie = testing.mean_test(testData, meanMovie, 1, 2)

    trainPerson = dh.sort(trainData, 0)
    meanPerson = dh.average(trainPerson, 0, 2, 671)
    testPerson = testing.mean_test(testData, meanPerson, 0, 2)


def q3b(movFeat, trainData, testData):

    V = np.delete(movFeat, (0), axis=1)
    print lr.linear_reg(trainData, V, testData, 0)

def q3c(movFeat, trainData, testData):

    V = np.delete(movFeat, (0), axis=1)
    V = dh.pca_transform(V, 3)
    print lr.linear_reg(trainData, V, testData, 2)

def q3d(movFeat, trainData, testData):

    iterations = 1000000
    alphaScale = 0.001
    lamdaList = [0.1, 0.01, 0.001]
    kList = [13, 14, 15]
    #k, lamda = lr.fold_cv_error(testData, trainData, lamdaList, kList, 11667, iterations, alphaScale)
    k = 14
    lamda = 0.001
    trainError, testError, x, theta = lr.collab_filter(trainData, testData, k, lamda, alphaScale, iterations, True)

    ratings = np.dot(theta.T, x)
    trainError = testing.collab_test(ratings, trainData)
    testError = testing.collab_test(ratings, testData)

    print "k: ", k, " lamda: ", lamda, " trainError: ", trainError, " testError: ", testError, " iterations: ", iterations, " alphaScale: ", alphaScale
    xVal = xrange(0, iterations, iterations/100)

    plt.figure()
    plt.title("title")
    plt.ylabel("ylabel")
    plt.xlabel("xlabel")

    plt.scatter(xVal, testError, s=1, color='red')
    plt.scatter(xVal, trainError, s=1, color='cyan')

    plt.show()

if __name__ == "__main__":
    main()
