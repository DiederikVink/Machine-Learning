import numpy as np
import time
import Queue
import threading
from sklearn import svm
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
            (trainX, y, gamma, k, C, fold) = processQueue.get()
            print "Thread: ", threadID, " processing: ", gamma
            queueLock.release()
            valError = cross_validation(trainX, y, gamma, C, fold)
            print "Thread: ", threadID, "done: ", valError
            queueLock.acquire()
            dataQueue.put((valError, gamma, k, C))
            queueLock.release()
        else:
            queueLock.release()

        

def margin_svm(trainMatrix, testMatrix, PCA):
    # extract 2 and 8
    twoMatrix, twoY = dh.extract_value(trainMatrix, 2, -1)
    eightMatrix, eightY = dh.extract_value(trainMatrix, 8, 1)
    
    # create X and Y vectors
    trainY = np.append(twoY, eightY, axis = 0)
    trainX = np.append(twoMatrix, eightMatrix, axis = 0)

    # extract 2 and 8
    twoMatrix, twoY = dh.extract_value(testMatrix, 2, -1)
    eightMatrix, eightY = dh.extract_value(testMatrix, 8, 1)
    
    # create X and Y vectors
    testY = np.append(twoY, eightY, axis = 0)
    testX = np.append(twoMatrix, eightMatrix, axis = 0)

    gammaList = []
    min = 0.0
    max = 0.1
    step = (max-min)/10
    for i in np.arange(min+step,max+step,step):
        gammaList.append(i)
    fold = 100

    if PCA:
        kList = [3, 4, 5]
        cList = [1, 2, 3]
    else:
        kList = [256]
        cList = [1]


    gamma, k, C, runTime, valErrors = hard_margin_cv_error(trainX, trainY, testX, gammaList, kList, cList, fold)
    if PCA:
        trainXIn = dh.pca_transform(trainX, k)
        testXIn = dh.pca_transform(testX, k)
    else:
        trainXIn = trainX
        testXIn = testX
    testSVMY, trainSVMY = SVM_run(trainXIn, trainY, testXIn, kernel='rbf', gamma=gamma, C=C)
    
    trainError = error_calc(trainSVMY, trainY)
    testError = error_calc(testSVMY, testY)

    return testError, trainError, gamma, C, k, runTime, valErrors

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
    
        testRes, trainRes = SVM_run(trainSet, trainY, testSet, kernel='rbf', gamma=gam, C=C)
        totalError += error_calc(testRes, testY)
    
    return totalError/(trainX.shape[0]/fold)

def hard_margin_cv_error(trainX, y, testX, gammaList, kList, cList, fold):
    minError = 10000
    minGamma = 1

    workQueue = Queue.Queue(len(gammaList))
    dataQueue = Queue.Queue(len(gammaList))
    threads = []
    threadNum = 10

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
        if k = 256:
            trainXin = trainX
        else:
            trainXIn = dh.pca_transform(trainX, k)
        for C in cList:
            for gam in gammaList:
                workQueue.put((trainXIn, y, gam, k, C, fold))
    queueLock.release()

    while not workQueue.empty():
        pass

    global exitPoint
    exitPoint = 1

    for thread in threads:
        thread.join()

    runTime = time.time() - start
    valErrors = dh.extract_from_queue(dataQueue) 

    gamma, k, C = min(valErrors.values())

    #for gamma, valError in valErrors.iteritems():
    #    if (valError <= minError):
    #        minError = valError
    #        minGamma = gam

    #gamma = minGamma

    return gamma, k, C, runTime, valErrors

def SVM_run(trainX, y, testX, kernel, gamma, C):
    rbf = svm.SVC(kernel=kernel, shrinking=False, gamma=gamma, C=C).fit(trainX, y.ravel())
    trainRes = rbf.predict(trainX)
    testRes = rbf.predict(testX)
    return testRes, trainRes

def error_calc(svmY, y):
    diff = svmY + y.ravel()
    errorSum = np.sum([1 if val == 0 else 0 for val in diff.ravel()])
    return errorSum/float(len(diff))


