import numpy as np
import time
import Queue
import threading
from sklearn import svm
from sklearn import preprocessing
import data_handler as dh

exitPoint = 0
queueLock = threading.Lock()

class cvThread (threading.Thread):
    def __init__(self, threadID, processQueue, dataQueue):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.processQueue = processQueue
        self.dataQueue = dataQueue
    def run(self):
        #print "Starting thread: ", self.threadID
        cv_thread_setup(self.threadID, self.processQueue, self.dataQueue)
        #print "Finished thread: ", self.threadID

def cv_thread_setup (threadID, processQueue, dataQueue):
    while not exitPoint:
        queueLock.acquire()
        if not processQueue.empty():
            (trainX, y, gamma, C, k, fold) = processQueue.get()
            #print "Thread: ", threadID, " processing: ", gamma
            queueLock.release()
            valError = cross_validation(trainX, y, gamma, C, fold)
            #print "Thread: ", threadID, "done: ", valError
            queueLock.acquire()
            dataQueue.put((valError, gamma, C, k))
            queueLock.release()
        else:
            queueLock.release()

        

def margin_svm(trainMatrix, testMatrix, PCA, matrixList1, matrixList2, gammaMin, gammaMax, gNum, cMin, cMax, cNum, PCAmin, PCAmax, PCAnum):
    # extract 2 and 8
    twoMatrix, twoY = dh.extract_value(trainMatrix, matrixList1, -1)
    eightMatrix, eightY = dh.extract_value(trainMatrix, matrixList2, 1)
    
    # create X and Y vectors
    trainY = np.append(twoY, eightY, axis = 0)
    trainX = np.append(twoMatrix, eightMatrix, axis = 0)

    # extract 2 and 8
    twoMatrix, twoY = dh.extract_value(testMatrix, matrixList1, -1)
    eightMatrix, eightY = dh.extract_value(testMatrix, matrixList2, 1)
    
    testY = np.append(twoY, eightY, axis = 0)
    testX = np.append(twoMatrix, eightMatrix, axis = 0)

    testXnorm = testX
    trainXnorm = trainX

    gammaList = []
    step = (gammaMax-gammaMin)/gNum
    for i in np.arange(gammaMin+step,gammaMax+0.000000000001,step):
        gammaList.append(i)
    fold = 100

    if PCA:
        testXnorm = testX - np.mean(testX)
        #testXnorm = preprocessing.scale(testX)
        trainXnorm = trainX - np.mean(trainX)
        #trainXnorm = preprocessing.scale(trainX)

        cList = []
        step = (cMax-cMin)/cNum
        for i in np.arange(cMin+step, cMax+0.00000000001, step):
            cList.append(i)

        if PCA == 1:
            kList = []
            PCAstep = (PCAmax - PCAmin)/PCAnum
            for i in xrange(PCAmin+PCAstep, PCAmax+1, PCAstep):
                kList.append(i)
        elif PCA == 2:
            kList = [2]
        elif PCA == 3:
            kList = [256]
    else:
        cList = [1]
        kList = [256]

    trainXIn = trainXnorm
    testXIn = testXnorm

    runTime, valErrors = hard_margin_cv_error(trainXIn, trainY, testXIn, gammaList, cList, kList, fold)
    

    trainError = {}
    testError = {}
    cvError = {}

    for k, gammaDict in valErrors.items():

        C, gamma = min(gammaDict, key=gammaDict.get)
        if PCA:
            PCAMatrix = dh.pca_transform(trainXnorm, k)
            trainXIn = PCAMatrix.transform(trainXnorm)
            #trainXIn = preprocessing.scale(trainXIn)
            testXIn = PCAMatrix.transform(testXnorm)
            #testXIn = preprocessing.scale(testXIn)
        else:
            trainXIn = trainXnorm
            testXIn = testXnorm
        testSVMY, trainSVMY, rbf = SVM_run(trainXIn, trainY, testXIn, kernel='rbf', gamma=gamma, C=C)
        trainError.update({k: error_calc(trainSVMY, trainY)})
        testError.update({k: error_calc(testSVMY, testY)})
        cvError.update({k: gammaDict[(C, gamma)]})

    return rbf, trainSVMY, testSVMY, trainXIn, testXIn, trainY, testY, testError, trainError, cvError, gamma, C, k, runTime, valErrors

def cross_validation(trainX, y, gam, C, fold):
    totalError = 0
    
    for i in xrange(0, trainX.shape[0]-fold, fold):
        trainSet = trainX
        trainY = y
    
        for value in xrange(0, fold):
            trainSet = np.delete(trainSet, (i), axis = 0)
            trainY = np.delete(trainY, (i), axis = 0)
    
        testSet = trainX[i:i+fold,:]
        testY = y[i:i+fold,:]
    
        #trainSet = preprocessing.scale(trainSet)
        #testSet = preprocessing.scale(testSet)

        testRes, trainRes, rbf = SVM_run(trainSet, trainY, testSet, kernel='rbf', gamma=gam, C=C)
        totalError += error_calc(testRes, testY)
    
    return totalError/(trainX.shape[0]/fold)

def hard_margin_cv_error(trainX, y, testX, gammaList, cList, kList, fold):
    minError = 10000
    minGamma = 1

    workQueue = Queue.Queue(len(gammaList) * len(cList) * len(kList))
    dataQueue = Queue.Queue(len(gammaList) * len(cList) * len(kList))
    with workQueue.mutex:
        dataQueue.queue.clear()
    threads = []
    threadNum = 4

    # start thread for each gamma
    for threadID in xrange(1,threadNum+1):
        #start = time.time()
        #valError = cross_validation(trainX, y, gam, fold)
        #if (valError <= minError):
        #    minError = valError
        #    minGamma = gam

        tmpThread = cvThread(threadID, workQueue, dataQueue)
        tmpThread.start()
        threads.append(tmpThread)

    start = time.time()

    # start filling queue
    queueLock.acquire()
    for k in kList:
        if k == 256:
            trainXIn =  trainX
        else:
            PCAMat = dh.pca_transform(trainX, k)
            trainXIn = PCAMat.transform(trainX)
        for C in cList:
            for gam in gammaList:
                workQueue.put((trainXIn, y, gam, C, k, fold))
    queueLock.release()

    while not workQueue.empty():
        pass

    global exitPoint
    exitPoint = 1

    for thread in threads:
        thread.join()

    runTime = time.time() - start
    valErrors = dh.extract_from_queue(dataQueue) 

    exitPoint = 0

    return runTime, valErrors

def SVM_run(trainX, y, testX, kernel, gamma, C):
    rbf = svm.SVC(kernel=kernel, shrinking=False, gamma=gamma, C=C).fit(trainX, y.ravel())
    trainRes = rbf.predict(trainX)
    testRes = rbf.predict(testX)
    return testRes, trainRes, rbf

def error_calc(svmY, y):
    diff = svmY + y.ravel()
    errorSum = np.sum([1 if val == 0 else 0 for val in diff.ravel()])
    return errorSum/float(len(diff))


