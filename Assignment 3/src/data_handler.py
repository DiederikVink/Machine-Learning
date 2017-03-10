import csv
import scipy
import numpy as np
from sklearn import decomposition, preprocessing

def read_data(fileName):
    dataMatrix = np.loadtxt(open(fileName, "rb"), delimiter=",", skiprows=1)
    return dataMatrix

def sort(dataMatrix, index):
    return dataMatrix[dataMatrix[:,index].argsort()]

def average(dataMatrix, index, data, total):
    movie = 1;
    val_sum = []
    mean = np.array([[0,0]])

    for row in dataMatrix:
        if (row[index] == movie):
            val_sum.append(row[data])
        else:
            mean = append_zeros(row[index], mean, val_sum, movie)
            val_sum = []
            movie = row[index]
            val_sum.append(row[data])

    mean = append_zeros(row[index]+1, mean, val_sum, movie)

    if (movie < total):
        mean = append_zeros(total+1, mean, [], row[index]+1)
    mean = np.delete(mean, (0), axis=0)
    return mean

def append_zeros(rindex, mean, val_sum, movie):
    mean = np.concatenate((mean, [[movie,np.nan_to_num(np.mean(val_sum))]]))
    while(rindex-1 != movie):
        movie += 1
        mean = np.concatenate((mean, [[movie,0]]))
    return mean

def extract(dataMatrix, index):
    val = dataMatrix[0, index]
    count = 0
    bound = []
    for row in dataMatrix[:,index]:
        if row != val:
            bound.append(count-1)
            val = row
        count += 1
    bound.append(count-1)
    return bound

def normalize(dataMatrix):
    mean = np.mean(dataMatrix, axis = 0)
    stdev = np.std(dataMatrix, axis = 0)
    tmp = dataMatrix - mean
    return tmp/stdev

def unnormalize(dataMatrix):
    mean = np.mean(dataMatrix, axis = 0)
    stdev = np.std(dataMatrix, axis = 0)
    tmp = dataMatrix * stdev
    return tmp + mean

def calc_H(lamda, Z):
    ZT = np.transpose(Z)
    ZTZ = np.dot(ZT,Z)

    LI = np.zeros((ZTZ.shape[0],ZTZ.shape[1]))
    np.fill_diagonal(LI, lamda)
    
    ZTZLI = ZTZ + LI
    ZTZLI_1 = np.linalg.inv(ZTZLI)
    ZTZLI_1ZT = np.dot(ZTZLI_1,ZT)
    return np.dot(Z,ZTZLI_1ZT)

def regular_transform(dataMatrix, n):
    trans = dataMatrix
    for degree in xrange(2,n+1):
        trans = np.append(trans, np.power(dataMatrix, n), axis=1)
    return trans

def pca_transform(dataMatrix, n):
    PCA = decomposition.PCA(n_components=n)
    trans = PCA.fit_transform(dataMatrix)
    return trans

def legendre_transform(dataMatrix, n):
    trans = np.zeros((dataMatrix.shape[0], 1))
    for degree in xrange(0,n+1):
        transLeg = np.polyval(scipy.special.legendre(degree),dataMatrix)
        trans = np.append(trans, transLeg, axis = 1)

    trans = np.delete(trans, (0), axis = 1)
    return trans

def polynomialization(dataMatrix, n):
    poly = preprocessing.PolynomialFeatures(n, interaction_only=True)
    V = poly.fit_transform(dataMatrix)
    return V
