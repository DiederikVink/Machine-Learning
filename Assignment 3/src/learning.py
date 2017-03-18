import numpy as np
import data_handler as dh
from sklearn import preprocessing
import random
import testing
import time

def fold_cv_error(testMatrix, trainMatrix, lamdaList, kList, fold, iterations, alphaScale, LList):
    minError = 10000
    minK = 1
    minLamda = 1
    minL = 1

    L = 2
    k = 8

    for lamda in lamdaList:
        totalError = 0
    
        start = time.time()
        for i in xrange(0, trainMatrix.shape[0]-fold, fold):
            trainSet = trainMatrix
            for value in xrange(0,fold):
                trainSet = np.delete(trainSet, (i), axis = 0)
            
            testSet = trainMatrix[i:i+fold,:]
            trainErrorList, testErrorList, x, theta = collab_filter(trainSet, testMatrix, k, lamda, alphaScale, iterations, False, L)
    
            ratings = np.dot(theta.T, x)
            testError = testing.collab_test(ratings, testSet)
    
            totalError += testError
        valError = totalError/(trainMatrix.shape[0]/fold)
        if (valError <= minError):
             minError = valError
             minLamda = lamda
        print "\tlamda:", lamda, "\tk:", k, "\tlasso: ", L, "\terror:", valError, "\ttime: ", time.time() - start

    lamda = minLamda

    minError = 10000

    for k in kList:
        totalError = 0

        start = time.time()
        for i in xrange(0, trainMatrix.shape[0]-fold, fold):
            trainSet = trainMatrix
            for value in xrange(0,fold):
                trainSet = np.delete(trainSet, (i), axis = 0)
            
            testSet = trainMatrix[i:i+fold,:]
            trainErrorList, testErrorList, x, theta = collab_filter(trainSet, testMatrix, k, lamda, alphaScale, iterations, False, L)

            ratings = np.dot(theta.T, x)
            testError = testing.collab_test(ratings, testSet)

            totalError += testError
        valError = totalError/(trainMatrix.shape[0]/fold)
        if (valError <= minError):
             minError = valError
             minK = k
        print "\tlamda:", lamda, "\tk:", k, "\tlasso: ", L, "\terror:", valError, "\ttime: ", time.time() - start

    k = minK

    #for L in LList:
    #    totalError = 0
    #
    #    start = time.time()
    #    for i in xrange(0, trainMatrix.shape[0]-fold, fold):
    #        trainSet = trainMatrix
    #        for value in xrange(0,fold):
    #            trainSet = np.delete(trainSet, (i), axis = 0)
    #        
    #        testSet = trainMatrix[i:i+fold,:]
    #        trainErrorList, testErrorList, x, theta = collab_filter(trainSet, testMatrix, k, lamda, alphaScale, iterations, False, L)
    #
    #
    #        ratings = np.dot(theta.T, x)
    #        testError = testing.collab_test(ratings, testSet)
    #
    #        totalError += testError
    #    valError = totalError/(trainMatrix.shape[0]/fold)
    #    if (valError <= minError):
    #         minError = valError
    #         minL = L
    #    print "\tlamda:", lamda, "\tk:", k, "\tlasso: ", L, "\terror:", valError, "\ttime: ", time.time() - start

    #L = minL
    minError = 10000

    return (k, lamda, L)

def collab_filter(trainMatrix, testMatrix, k_val, lamda, alpha, iterLimit, Graph, L):
    userSort = dh.sort(trainMatrix, 0)
    movieSort = dh.sort(trainMatrix, 1)
    userBounds = dh.extract(userSort, 0)
    movieBounds = dh.extract(movieSort, 1)

    weights = np.random.rand(k_val, 671)
    movFeat = np.random.rand(k_val, 9066)

    userBounds = [-1] + userBounds
    movieBounds = [-1] + movieBounds
    
    (trainError, testError, x, theta) = SGD(alpha, lamda, weights, movFeat, userSort, userBounds, movieSort, movieBounds, iterLimit, testMatrix, trainMatrix, Graph, L)

    return trainError, testError, x, theta

def SGD(alphaScale, lamda, theta, x, userSort, userBounds, movieSort, movieBounds, iterLimit, testMatrix,trainMatrix, Graph, L):
    xNew = x
    thetaNew = theta
    trainError = []
    testError = []
    userCount = 1
    movCount = 1
    for i in xrange(0, iterLimit + 1):
        #mov = random.randint(1, len(movieBounds)-1)
        mov = movCount
        movCount += 1
        if (movCount == len(movieBounds)):
            movCount = 1
        movRandVal = random.randint(movieBounds[mov-1]+1, movieBounds[mov])
        movUser = movieSort[movRandVal,0]
        movCurrent = movieSort[movRandVal,1]
        movTheta = theta[:,int(movUser)-1]
        movX = x[:,int(movCurrent)-1]
        movY = movieSort[movRandVal, 2]

        movAbsError = abs_calc(movTheta, movX, movY)
        
        block1 = movTheta * movAbsError
        if (L == 1):
            block2 = block1 + lamda * np.sign(movX)
        else:
            block2 = block1 + lamda * movX
            
        #alpha = alphaScale * np.linalg.norm(block2)
        alpha = alphaScale
        block3 = block2 * alpha
        block3 = np.array([movX - block3])
        xNew[:,int(movCurrent)-1] = block3.T[:,0]
        
        #user = random.randint(1, len(userBounds)-1)
        user = userCount
        userCount += 1
        if (userCount == len(userBounds)):
            userCount = 1
        #user = movRandVal
        #userRandVal = mov
        userRandVal = random.randint(userBounds[user-1]+1, userBounds[user])
        userChoice = userSort[userRandVal,1]
        userCurrent = userSort[userRandVal,0]
        userTheta = theta[:,int(userCurrent)-1]
        userX = x[:,int(userChoice)-1]
        userY =  userSort[userRandVal, 2]
        
        userAbsError = abs_calc(userTheta, userX, userY)

        block1 = userX * userAbsError
        if (L == 1):
            block2 = block1 + lamda * np.sign(userTheta)
        else:
            block2 = block1 + lamda * userTheta 

        #alpha = alphaScale * np.linalg.norm(block2)
        alpha = alphaScale
        block3 = block2 * alpha
        block3 = np.array([userTheta - block3])
        thetaNew[:,int(userCurrent)-1] = block3.T[:,0]

        x = xNew
        theta = thetaNew
        if Graph:
            if (i % (iterLimit/100) == 0):
                ratings = np.dot(theta.T, x)
                testError.append(testing.collab_test(ratings, testMatrix))
                trainError.append(testing.collab_test(ratings, trainMatrix))
    return trainError, testError, x, theta

def abs_calc(theta, x, y):
    return np.dot(theta.T, x) - y


def linear_reg(dataMatrix, V, testMatrix, legen):
    trainPerson = dh.sort(dataMatrix, 0)
    bounds = dh.extract(trainPerson, 0)

    if (legen == 0):
        Z = V
        lamda = gen_lamda()
        (uLamda, uError) = lamda_cv(Z, lamda, bounds, dataMatrix)
        (rRegW, ymean) = regression(Z, uLamda, bounds, trainPerson)
        V = preprocessing.scale(Z)
        testLinReg = testing.lin_reg_test(rRegW, V, testMatrix, ymean, 0, 1, 2)
        trainLinReg = testing.lin_reg_test(rRegW, V, dataMatrix, ymean, 0, 1, 2)
        return testLinReg, trainLinReg
    elif (legen == 1):
        (bestLegen, uLamda) = legendre_cv(V, bounds, dataMatrix, 10)
        Z = dh.legendre_transform(V, bestLegen)
        (rRegW, ymean) = regression(Z, uLamda, bounds, trainPerson)
        V = preprocessing.scale(Z)
        testLinReg = testing.lin_reg_test(rRegW, V, testMatrix, ymean, 0, 1, 2)
        trainLinReg = testing.lin_reg_test(rRegW, V, dataMatrix, ymean, 0, 1, 2)
        return bestLegen, testLinReg, trainLinReg
    elif (legen == 2):
        V = dh.pca_transform(V, 4)
        (bestLegen, uLamda) = poly_cv(V, bounds, dataMatrix, 4)
        Z = dh.polynomialization(V, bestLegen)
        (rRegW, ymean) = regression(Z, uLamda, bounds, trainPerson)
        V = preprocessing.scale(Z)
        testLinReg = testing.lin_reg_test(rRegW, V, testMatrix, ymean, 0, 1, 2)
        trainLinReg = testing.lin_reg_test(rRegW, V, dataMatrix, ymean, 0, 1, 2)
        return bestLegen, testLinReg, trainLinReg

    else:
        return 0

def gen_lamda():
    minim = 0.0
    maxim = 10000.0
    step = (maxim-minim)/10
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

def poly_cv(V, bounds, dataMatrix, n):
    legList = np.zeros((n-1, len(bounds)))
    allLamda = np.zeros((len(bounds),1))
    for degree in xrange(2, n+1):
        ECV = np.zeros(len(bounds))
        Vtrans = dh.polynomialization(V, degree)
        #print Vtrans.shape
        lamda = gen_lamda()
        uLamda, minError = lamda_cv(Vtrans, lamda, bounds, dataMatrix)
        allLamda = np.append(allLamda, uLamda, axis = 1)

        prevBound = 0
        i = 0
        for bound in bounds:
            Z = np.zeros((1,Vtrans.shape[1]))
            y = np.array([dataMatrix[prevBound:bound+1, 2]]).T
            tmp = dataMatrix[prevBound:bound+1, 1]
            prevBound = bound+1
            for val in tmp:
                Z = np.append(Z, [Vtrans[int(val-1),:]], axis=0)
            Z = np.delete(Z, (0), axis=0)

            Znorm = preprocessing.scale(Z)
            ycent = y - np.mean(y)

            (uLam, ECV[i]) = analytic_cv_error(Znorm, uLamda[i], ycent)
            i += 1
        legList[degree-2] = ECV
    allLamda = np.delete(allLamda, (0), axis = 1)
    minList = np.argmin(legList, axis=0)
    count = np.argmax(np.bincount(minList))
    return (count+2, allLamda[:,count])


def legendre_cv(V, bounds, dataMatrix, n):
    legList = np.zeros((n-1, len(bounds)))
    allLamda = np.zeros((len(bounds),1))
    for degree in xrange(2, n+1):
        ECV = np.zeros(len(bounds))
        Vtrans = dh.legendre_transform(V, degree)
        lamda = gen_lamda()
        uLamda, minError = lamda_cv(Vtrans, lamda, bounds, dataMatrix)
        allLamda = np.append(allLamda, uLamda, axis = 1)

        prevBound = 0
        i = 0
        for bound in bounds:
            Z = np.zeros((1,Vtrans.shape[1]))
            y = np.array([dataMatrix[prevBound:bound+1, 2]]).T
            tmp = dataMatrix[prevBound:bound+1, 1]
            prevBound = bound+1
            for val in tmp:
                Z = np.append(Z, [Vtrans[int(val-1),:]], axis=0)
            Z = np.delete(Z, (0), axis=0)

            Znorm = preprocessing.scale(Z)
            ycent = y - np.mean(y)

            (uLam, ECV[i]) = analytic_cv_error(Znorm, uLamda[i], ycent)
            i += 1
        legList[degree-2] = ECV
    allLamda = np.delete(allLamda, (0), axis = 1)
    minList = np.argmin(legList, axis=0)
    count = np.argmax(np.bincount(minList))
    return (count+2, allLamda[:,count])

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

        (minLamda, minError) = analytic_cv_error(Znorm, lamda, ycent)
        userLamda = np.append(userLamda, [[minLamda]], axis=0)

    userLamda = np.delete(userLamda, (0), axis=0)
    return userLamda, minError

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
    return (minLamda, minError)

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

#def SGD(alpha, lamda, theta, x, userSort, userBounds, movieSort, movieBounds, iterLimit, testMatrix,trainMatrix, Graph):
#    xNew = x
#    thetaNew = theta
#    trainError = []
#    testError = []
#    for i in xrange(0, iterLimit + 1):
#        #thetaNew = np.zeros((theta.shape[0],1))
#        for user in xrange(1, len(userBounds)):
#            userRandVal = random.randint(userBounds[user-1]+1, userBounds[user])
#            userChoice = userSort[userRandVal,1]
#            userCurrent = userSort[userRandVal,0]
#            userTheta = theta[:,int(userCurrent)-1]
#            userX = x[:,int(userChoice)-1]
#            userY =  userSort[userRandVal, 2]
#            
#            userAbsError = abs_calc(userTheta, userX, userY)
#
#            block1 = userX * userAbsError
#            block2 = block1 + lamda * userTheta 
#            block3 = block2 * alpha
#            block3 = np.array([userTheta - block3])
#            thetaNew[:,int(userCurrent)-1] = block3.T[:,0]
#            #thetaNew = np.append(thetaNew, block3.T, axis=1)
#        #thetaNew = np.delete(thetaNew, (0), axis = 1)
#
#        for mov in xrange(1, len(movieBounds)):
#            movRandVal = random.randint(movieBounds[mov-1]+1, movieBounds[mov])
#            movUser = movieSort[movRandVal,0]
#            movCurrent = movieSort[movRandVal,1]
#            movTheta = theta[:,int(movUser)-1]
#            movX = x[:,int(movCurrent)-1]
#            movY = movieSort[movRandVal, 2]
#
#            movAbsError = abs_calc(movTheta, movX, movY)
#            
#            block1 = movTheta * movAbsError
#            block2 = block1 + lamda * movX
#            block3 = block2 * alpha
#            block3 = np.array([movX - block3])
#            xNew[:,int(movCurrent)-1] = block3.T[:,0]
#        
#        x = xNew
#        theta = thetaNew
#        if Graph:
#            if (i % 50 == 0):
#                ratings = np.dot(theta.T, x)
#                testError.append(testing.collab_test(ratings, testMatrix))
#                trainError.append(testing.collab_test(ratings, trainMatrix))
#    return trainError, testError, x, theta
