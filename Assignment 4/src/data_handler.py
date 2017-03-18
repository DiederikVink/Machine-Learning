import csv
import numpy as np

def read_data(fileName):
    dataMatrix = np.loadtxt(open(fileName, "rb"))
    return dataMatrix

def extract_value(matrix, value, classification):
    valMatrix = np.zeros((1,matrix.shape[1]-1))
    for row in matrix:
        if row[0] == value:
            valMatrix = np.append(valMatrix, [row[1:]], axis=0)
    valMatrix = np.delete(valMatrix, (0), axis=0)
    valVector = classification * np.ones((valMatrix.shape[0],1))
    return valMatrix, valVector


def extract_from_queue(queue):
    data = {}
    while True:
        try:
            error, gamma = queue.get(block=False)
        except:
            break
        else:
            data.update({gamma:error})
    return data
