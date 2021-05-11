from pyabf import ABF
import os
import eventDetect
from datetime import datetime
import sys
import time

from multiprocessing import Pool


def detectMainFast(fileList, pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration):
    start = time.clock()
    fileName = fileList
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime + '.txt'

    po = Pool(8)
    fileNumber = 0

    for i in range(len(fileName)):
        abf = ABF(fileName[i])
        fileNumber += 1
        current = abf.data[0]
        iterNumber = int(len(current) / (abf.dataRate * 10)) + 1
        if (pattern == "down") or (pattern == "DOWN"):
            for i in range(iterNumber):
                if i == 0:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[i * abf.dataRate * 10:i * abf.dataRate * 10 + abf.dataRate * 10], startCoeff, endCoeff,
                                    filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
                elif i != iterNumber - 1:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[i * abf.dataRate * 10 - 1000:i * abf.dataRate * 10 + abf.dataRate * 10], startCoeff, endCoeff,
                                    filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
                else:
                    po.apply_async(eventDetect.eventDownFast,
                                   (current[i * abf.dataRate * 10:], startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,
                                    resultName, abf.dataRate, fileNumber, i,))
        elif (pattern == "up") or (pattern == "UP"):
            for i in range(iterNumber):
                if i == 0:
                    po.apply_async(eventDetect.eventUpFast,
                                   (current[i * abf.dataRate * 10:i * abf.dataRate * 10 + abf.dataRate * 10], startCoeff,
                                   endCoeff, filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
                elif i != iterNumber - 1:
                    po.apply_async(eventDetect.eventUpFast,
                                   (current[i * abf.dataRate * 10 - 1000:i * abf.dataRate * 10 + abf.dataRate * 10],
                                    startCoeff, endCoeff,
                                    filterCoeff, minDuration, maxDuration, resultName, abf.dataRate, fileNumber, i,))
                else:
                    po.apply_async(eventDetect.eventUpFast,
                                   (current[i * abf.dataRate * 10:], startCoeff, endCoeff, filterCoeff, minDuration, maxDuration,
                                    resultName, abf.dataRate, fileNumber, i,))
        else:
            po.close()
            sys.exit(1)

    po.close()
    po.join()
    elapsed = (time.clock() - start)
    print("Time used:", elapsed)
    print('finish')


def detectMain(pattern, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration):
    path = "data/"
    fileName = os.listdir(path)
    nowTime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if not os.path.exists('result/'):
        os.makedirs('result/')
    resultName = 'result/' + nowTime + '.txt'

    for i in range(len(fileName)):
        abf = ABF(path + fileName[i])
        current = abf.data[0]
        if pattern == "down":
            eventDetect.eventDownFast(current, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, resultName,
                                      abf.dataRate)
        elif pattern == "up":
            eventDetect.eventUpFast(current, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, resultName,
                                      abf.dataRate)
        else:
            sys.exit(1)

    print('finish')
