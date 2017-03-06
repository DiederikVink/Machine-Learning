import numpy as np
import data_handler as dh
from sklearn import preprocessing
import testing
import time

def linear_reg(dataMatrix, V, testMatrix, legen):
    trainPerson = dh.sort(dataMatrix, 0)
    bounds = dh.extract(trainPerson, 0)

    if (legen == 0):
        Z = V
        lamda = gen_lamda()
        uLamda = lamda_cv(Z, lamda, bounds, dataMatrix)
        (rRegW, ymean) = regression(Z, uLamda, bounds, trainPerson)
        V = preprocessing.scale(Z)
        testLinReg = testing.lin_reg_test(rRegW, V, testMatrix, ymean, 0, 1, 2)
        return testLinReg
    elif (legen == 1):
        legendre_cv(  )
        return 1
    else:
        return 0

def gen_lamda():
    minim = 0.0
    maxim = 10000.0
    step = (maxim-minim)/100
    lamda = list(np.arange(minim+step,maxim+step,step))
    return lamda


def regression(V, lamda, bounds, dataMatrix):
    prevBound = 0
    rRegW = np.zeros((V.shape[1],1))
    minErr = 10000
    i = 0
    ymean = np.zeros((1,1))
    for bound in bounds:
        Z = np.zeros((1,V.shape[1]))
        y = np.array([dataMatrix[prevBound:bound+1, 2]]).T
        testMatrix = np.array([dataMatrix[prevBound:bound+1]])
        tmp = dataMatrix[prevBound:bound+1, 1]
        prevBound = bound+1

        for val in tmp:
            Z = np.append(Z, [V[int(val-1),:]], axis=0)
        Z = np.delete(Z, (0), axis=0)
       
        Znorm = preprocessing.scale(Z)
        yAvg = np.mean(y, axis = 0)
        ycent = y - yAvg
        ymean = np.append(ymean, [yAvg], axis=1)

        rRegW = np.append(rRegW, ridge_reg(Znorm, ycent, lamda[i]), axis=1)
        i += 1
    ymean = np.delete(ymean, (0), axis=1)
    rRegW = np.delete(rRegW, (0), axis = 1)
    return (rRegW, ymean)

def legendre_cv(V, lamda, bounds, dataMatrix, n):

    for degree in xrange(2, n+1):
        Z = dh.legendre_transform(V, degree)
        #lamda = gen_lamda()
        #uLamda = lamda_cv(Z, lamda, bounds, dataMatrix)



    
def lamda_cv(V, lamda, bounds, dataMatrix):
    prevBound = 0
    rRegW = np.zeros((V.shape[1],1))
    userLamda = np.zeros((1, 1))
    for bound in bounds:
        Z = np.zeros((1,V.shape[1]))
        y = np.array([dataMatrix[prevBound:bound+1, 2]]).T
        tmp = dataMatrix[prevBound:bound+1, 1]
        prevBound = bound+1

        for val in tmp:
            Z = np.append(Z, [V[int(val-1),:]], axis=0)
        Z = np.delete(Z, (0), axis=0)

        Znorm = preprocessing.scale(Z)
        ycent = y - np.mean(y)

        minLamda = analytic_cv_error(Znorm, lamda, ycent)
        userLamda = np.append(userLamda, [[minLamda]], axis=0)

    userLamda = np.delete(userLamda, (0), axis=0)
    return userLamda

def empirical_cv_error(Z, lamda, y):
    totalError = 0
    minError = 10000
    for lam in lamda:
        i = 0
        totalError = 0
        for row in Z:
            Ztmp = np.delete(Z, (i), axis = 0)
            ytmp = np.delete(y, (i), axis = 0)
            wtmp = ridge_reg(Ztmp, ytmp, lam)
            err = testing.cross_val_test(wtmp, row, y[i])
            totalError += err
            i += 1
        avgError = totalError / Z.shape[0]
        if (avgError <= minError):
            minError = avgError
            minLamda = lam
    return minLamda

def analytic_cv_error(Z, lamda, y):
    minError = 100000
    minLamda = 0
    for lam in lamda:
        H = dh.calc_H(lam, Z)
        yHat = np.dot(H,y)
        HDiag = np.array([H.diagonal()]).T
        denom = 1 - HDiag
        numer = yHat - y
        div = numer/denom
        divsq = np.square(div)
        sumdiv = np.sum(divsq)
        res = sumdiv/(Z.shape[0])
        if (res <= minError):
            minError = res
            minLamda = lam
    return minLamda

def ridge_reg(Z, y, lamda):
    ZT = np.transpose(Z)
    ZTZ = np.dot(ZT,Z)

    LI = np.zeros((ZTZ.shape[0],ZTZ.shape[1]))
    np.fill_diagonal(LI, lamda)
    
    ZTZLI = ZTZ + LI
    ZTZLI_1 = np.linalg.inv(ZTZLI)
    ZTZLI_1ZT = np.dot(ZTZLI_1,ZT)
    return np.dot(ZTZLI_1ZT,y)
    
def build_y(bounds, dataMatrix, nrows, ncols):
    y = np.zeros((nrows, ncols))
    i = 0
    prevBound = 0
    for bound in bounds:
        tmp = dataMatrix[prevBound:bound+1, 1:3]
        prevBound = bound+1
        for row in tmp:
            y[row[0]-1, i] = row[1]
        i += 1
    return y
