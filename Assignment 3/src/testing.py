import numpy as np

def mean_test(dataMatrix, meanMatrix, index, data):
    errList = [meanMatrix[row[index]-1,1] - row[data] for row in dataMatrix]
    errSquare = np.square(errList)
    err = np.sum(errSquare)
    return err/dataMatrix.shape[0]

def lin_reg_test(w, v, r, user, movie, rating):
    rHat = np.dot(np.transpose(w), np.transpose(v))
    errList = [row[rating] - rHat[row[user]-1][row[movie]-1] for row in r]
    errSquare = np.square(errList)
    err = np.sum(errSquare)
    return err/r.shape[0]

def cross_val_test(w, z, r):
    return np.square(r - np.dot(z, w))
