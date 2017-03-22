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
            (trainX, y, gamma, fold) = processQueue.get()
            print "Thread: ", threadID, " processing: ", gamma
            queueLock.release()
            valError = cross_validation(trainX, y, gamma, fold)
            print "Thread: ", threadID, "done: ", valError
            queueLock.acquire()
            dataQueue.put((valError, gamma))
            queueLock.release()
        else:
            queueLock.release()

        

def hard_margin_svm(trainMatrix, testMatrix):
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
    fold = 10

    gamma, runTime = hard_margin_cv_error(trainX, trainY, testX, gammaList, fold)
    testSVMY, trainSVMY = SVM_run(trainX, trainY, testX, kernel='rbf', gamma=gamma)
    
    trainError = error_calc(trainSVMY, trainY)
    testError = error_calc(testSVMY, testY)

    return testError, trainError, gamma, runTime

def cross_validation(trainX, y, gam, fold):
    totalError = 0
    
    for i in xrange(0, trainX.shape[0]-fold, fold):
        trainSet = trainX
        trainY = y
    
        for value in xrange(0, fold):
            trainSet = np.delete(trainSet, (i), axis = 0)
            trainY = np.delete(trainY, (i), axis = 0)
    
        testSet = trainX[i:i+fold,:]
        testY = y[i:i+fold,:]
    
        testRes, trainRes = SVM_run(trainSet, trainY, testSet, kernel='rbf', gamma=gam)
        totalError += error_calc(testRes, testY)
    
    return totalError/(trainX.shape[0]/fold)

def hard_margin_cv_error(trainX, y, testX, gammaList, fold):
    minError = 10000
    minGamma = 1

    workQueue = Queue.Queue(len(gammaList))
    dataQueue = Queue.Queue(len(gammaList))
    threads = []
    threadNum = 50

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
    for gam in gammaList:
        workQueue.put((trainX, y, gam, fold))
    queueLock.release()

    while not workQueue.empty():
        pass

    global exitPoint
    exitPoint = 1

    for thread in threads:
        thread.join()

    runTime = time.time() - start
    valErrors = dh.extract_from_queue(dataQueue) 

    gamma = min(valErrors, key=valErrors.get)

    #for gamma, valError in valErrors.iteritems():
    #    if (valError <= minError):
    #        minError = valError
    #        minGamma = gam

    #gamma = minGamma

    return gamma, runTime

def SVM_run(trainX, y, testX, kernel, gamma):
    rbf = svm.SVC(kernel=kernel, shrinking=False, gamma=gamma).fit(trainX, y.ravel())
    trainRes = rbf.predict(trainX)
    testRes = rbf.predict(testX)
    return testRes, trainRes

def error_calc(svmY, y):
    diff = svmY + y.ravel()
    errorSum = np.sum([1 if val == 0 else 0 for val in diff.ravel()])
    return errorSum/float(len(diff))


