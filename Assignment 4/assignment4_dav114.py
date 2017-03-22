import sys
sys.path.insert(0, './src')
import csv
import numpy as np
import scipy
import data_handler as dh
import learning as ln
import matplotlib.pyplot as plt

def main():
    q4a()
    #q4b()
    
def q4a():
    # extract data
    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    testError, trainError, gamma, C, k, runTime, valErrors = ln.margin_svm(trainMatrix, testMatrix, PCA=0)

    plt.figure()
    plt.title("Error vs Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Error")

    #plt.scatter(xVal, testErrorList, s=1, color='red', label="Test Error")
    #plt.scatter(xVal, trainErrorList, s=1, color='cyan', label="Train Error")
    
    data = []
    for error, listVals in valErrors.items():
        data.append({listVals[0], error})

    print data
    plt.scatter(data[0], data[1], s=1, color='red', label="TrainError");

    #plt.ylim(0.3,2)
    plt.legend()
    plt.show()

    print "gamma: ", gamma, "\ttime: ", runTime
    print "trainError: ", trainError, "\ttestError: ", testError

def q4b():

    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    testError, trainError, gamma, runTime, valErrors = ln.PCA_validation(trainMatrix, testMatrix)


if __name__ == '__main__':
    main()
