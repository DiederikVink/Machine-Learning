import sys
sys.path.insert(0, './src')
import csv
import numpy as np
import scipy
import data_handler as dh
import learning as ln

def main():
    q4a()
    
def q4a():
    # extract data
    trainMatrix = dh.read_data('./data/zip.train')
    testMatrix = dh.read_data('./data/zip.test')

    testError, trainError, gamma, runTime = ln.hard_margin_svm(trainMatrix, testMatrix)

    print "gamma: ", gamma, "\ttime: ", runTime
    print "trainError: ", trainError, "\ttestError: ", testError


if __name__ == '__main__':
    main()
