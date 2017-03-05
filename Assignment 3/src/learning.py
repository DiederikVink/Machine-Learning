import numpy as np
import data_handler as dh
import testing
import time

def linear_reg(dataMatrix, V, testMatrix):
    trainPerson = dh.sort(dataMatrix, 0)
    bounds = dh.extract(trainPerson, 0)
    Z = V
    minim = 0.0
    maxim = 10.0
    step = maxim/2.0
    lamda = list(np.arange(minim+step,maxim+step,step))
    uLamda = cross_validation(Z, lamda, bounds, dataMatrix)
    rRegW = regression(Z, uLamda, bounds, trainPerson)
    #testLinReg = testing.lin_reg_test(rRegW, Z, testMatrix, 0, 1, 2)
    #return testLinReg

def regression(V, lamda, bounds, dataMatrix):
    prevBound = 0
    rRegW = np.zeros((V.shape[1],1))
    minErr = 10000
    j = 0
    for bound in bounds:
        Z = np.zeros((1,V.shape[1]))
        y = np.array([dataMatrix[prevBound:bound+1, 2]]).T
        testMatrix = np.array([dataMatrix[prevBound:bound+1]])
        tmp = dataMatrix[prevBound:bound+1, 1]
        prevBound = bound+1

        for val in tmp:
            Z = np.append(Z, [V[val-1,:]], axis=0)
        Z = np.delete(Z, (0), axis=0)
       
        rRegW = np.append(rRegW, ridge_reg(Z, y, lamda), axis=1)
    rRegW = np.delete(rRegW, (0), axis = 1)
    return rRegW 
    
def cross_validation(V, lamda, bounds, dataMatrix):
    prevBound = 0
    rRegW = np.zeros((V.shape[1],1))
    userLamda = np.zeros((1, 1))
    for bound in bounds:
        Z = np.zeros((1,V.shape[1]))
        y = np.array([dataMatrix[prevBound:bound+1, 2]]).T
        tmp = dataMatrix[prevBound:bound+1, 1]
        prevBound = bound+1

        for val in tmp:
            Z = np.append(Z, [V[val-1,:]], axis=0)
        Z = np.delete(Z, (0), axis=0)
        
        totalError = 0
        minError = 10000
        for lam in lamda:
            i = 0
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
        userLamda = np.append(userLamda, [[minLamda]], axis=0)
    userLamda = np.delete(userLamda, (0), axis=0)
    return userLamda


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
