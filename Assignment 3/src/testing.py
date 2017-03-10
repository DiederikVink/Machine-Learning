import numpy as np

def mean_test(dataMatrix, meanMatrix, index, data):
    errList = [meanMatrix[int(row[index])-1,1] - row[data] if (meanMatrix[int(row[index])-1,1] != 0) else 0 for row in dataMatrix]
    errSquare = np.square(errList)
    nonZero = filter(lambda a: a != 0, errSquare)
    err = np.sum(errSquare)
    return err/len(nonZero)

def lin_reg_test(w, v, r, ymean, user, movie, rating):
    rHat = np.dot(v, w)
    rHat = rHat + ymean

    errList = [row[rating] - rHat[int(row[movie]-1)][int(row[user]-1)] for row in r]
    errSquare = np.square(errList)
    err = np.sum(errSquare)

    return err/r.shape[0]

def cross_val_test(w, z, r):
    return np.square(r - np.dot(z, w))

def collab_test(ratings, dataMatrix):
    errList = [row[2] - ratings[int(row[0]-1)][int(row[1]-1)] for row in dataMatrix]
    errSquare = np.square(errList)
    err = np.sum(errSquare)

    return err/dataMatrix.shape[0]

def collab_cv_error():
    totalError = 0
    minError = 10000
    
