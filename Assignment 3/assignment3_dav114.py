import sys
sys.path.insert(0, './src/')
import time
import numpy as np
import data_handler as dh
import testing
import learning as lr
np.set_printoptions(threshold=np.nan)


def main():
    trainData = dh.read_data('./movie-data/ratings-train.csv')
    testData = dh.read_data('./movie-data/ratings-test.csv')
    movFeat = dh.read_data('./movie-data/movie-features.csv')

    #q3a(trainData, testData)
    #q3b(movFeat, trainData, testData)    
    q3c(movFeat, trainData, testData)
    #q3d(movFeat, trainData, testData)


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

    lamdaList = [0.5, 0.25, 0.125, 0.0625]
    #lamda = lr.fold_cv_error(trainData, lamdaList, 10000)
    print lr.collab_filter(trainData, testData, 5, 0.001, 0.1, 100)

if __name__ == "__main__":
    main()
