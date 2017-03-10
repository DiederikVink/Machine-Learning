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
    trainErrorM = testing.mean_test(trainData, meanMovie, 1, 2)

    trainPerson = dh.sort(trainData, 0)
    meanPerson = dh.average(trainPerson, 0, 2, 671)
    testPerson = testing.mean_test(testData, meanPerson, 0, 2)
    trainErrorP = testing.mean_test(trainData, meanPerson, 0, 2)

    print "--------------------q3a-------------------------"
    print "Train Error for user: ", trainErrorP
    print "Test Error for user: ", testPerson
    print "Train Error for movie: ", trainErrorM
    print "Test Error for movie: ", testMovie


def q3b(movFeat, trainData, testData):

    V = np.delete(movFeat, (0), axis=1)
    print lr.linear_reg(trainData, V, testData, 0)

def q3c(movFeat, trainData, testData):

    V = np.delete(movFeat, (0), axis=1)
    #V = dh.pca_transform(V, 4)
    print lr.linear_reg(trainData, V, testData, 1)

def q3d(movFeat, trainData, testData):

    iterations = 500000
    alphaScale = 0.001
    lamdaList = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0005]
    kList = [4, 7, 10, 14]
    LList = [1, 2]
    k, lamda, L = lr.fold_cv_error(testData, trainData, lamdaList, kList, 3889, iterations, alphaScale, LList)
    #k = 10
    #lamda = 0.05
    #L = 2
    alphaScale = 0.0001
    iterations = 40000000
    trainErrorList, testErrorList, x, theta = lr.collab_filter(trainData, testData, k, lamda, alphaScale, iterations, True, L)

    ratings = np.dot(theta.T, x)
    trainError = testing.collab_test(ratings, trainData)
    testError = testing.collab_test(ratings, testData)

    print "k: ", k, " lamda: ", lamda, "lasso: ", L,  " trainError: ", trainError, " testError: ", testError, " iterations: ", iterations, " alphaScale: ", alphaScale
    xVal = xrange(0, iterations+1, iterations/100)

    plt.figure()
    plt.title("Error vs Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Error")

    plt.scatter(xVal, testErrorList, s=1, color='red', label="Test Error")
    plt.scatter(xVal, trainErrorList, s=1, color='cyan', label="Train Error")

    plt.ylim(0.3,2)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
