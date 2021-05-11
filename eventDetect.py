# -*- coding : utf-8 -*-
# coding: utf-8
import numpy as np
import scipy.signal


def eventDownFast(rawSignal, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, fileName, sampleRate, fileNumber, iterNumber):
    padLen = np.int64(sampleRate)
    prepadded = np.ones(padLen) * np.mean(rawSignal[0:1000])
    signalToFilter = np.concatenate((prepadded, rawSignal))
    rawSignal = np.array(rawSignal)

    mlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], signalToFilter)
    vlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], np.square(signalToFilter - mlTemp))

    ml = np.delete(mlTemp, np.arange(padLen))
    vl = np.delete(vlTemp, np.arange(padLen))

    sl = ml - startCoeff * np.sqrt(vl)
    Ni = len(rawSignal)
    points = np.array(np.where(rawSignal <= sl)[0])
    to_pop = np.array([])
    for i in range(1, len(points)):
        if points[i] - points[i - 1] == 1:
            to_pop = np.append(to_pop, i)
    to_pop = np.int64(to_pop)
    points = np.unique(np.delete(points, to_pop))
    NumberOfEvents = 0;
    RoughEventLocations = np.zeros((10000, 3))
    event_current = np.zeros((10000, 3))

    for i in points:
        event_start_mean = ml[i-100]
        if i >= Ni - 10:
            break;
        start = i
        El = ml[i] - endCoeff * np.sqrt(vl[i])
        while rawSignal[i + 1] < El and i <= Ni - 10:
            i = i + 1
        if ((minDuration * sampleRate / 1000) < (i + 1 - start)) and ((i + 1 - start) < (maxDuration * sampleRate / 1000)) and (event_start_mean - min(rawSignal[start:i + 1])) > 0:
            NumberOfEvents = NumberOfEvents + 1
            RoughEventLocations[NumberOfEvents - 1, 2] = i + 1 - start
            RoughEventLocations[NumberOfEvents - 1, 0] = start
            RoughEventLocations[NumberOfEvents - 1, 1] = i + 1
            event_current[NumberOfEvents - 1, 0] = (event_start_mean - min(rawSignal[start:i + 1]))
            event_current[NumberOfEvents - 1, 1] = event_start_mean
            event_current[NumberOfEvents - 1, 2] = abs(
                event_current[NumberOfEvents - 1, 0] / event_current[NumberOfEvents - 1, 1]) * 10000

    event_statistic = np.zeros((NumberOfEvents, 6))
    event_statistic[:, 0] = RoughEventLocations[0: NumberOfEvents, 2] / sampleRate * 1000
    event_statistic[:, 1:4] = event_current[0: NumberOfEvents, 0:3]
    if iterNumber == 0:
        event_statistic[:, 4] = (RoughEventLocations[0: NumberOfEvents, 0] + iterNumber * sampleRate * 10) * 1000 / sampleRate
    else:
        event_statistic[:, 4] = (RoughEventLocations[0: NumberOfEvents,
                                 0] + iterNumber * sampleRate * 10) * 1000 / sampleRate -10
    event_statistic[:, 5] = fileNumber
    with open(fileName, "a+") as fp:
        np.savetxt(fp, event_statistic, fmt='%.3f', delimiter="\t")


def eventUpFast(rawSignal, startCoeff, endCoeff, filterCoeff, minDuration, maxDuration, fileName, sampleRate, fileNumber, iterNumber):
    padLen = np.int64(sampleRate)
    prepadded = np.ones(padLen) * np.mean(rawSignal[0:1000])
    signalToFilter = np.concatenate((prepadded, rawSignal))
    rawSignal = np.array(rawSignal)

    mlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], signalToFilter)
    vlTemp = scipy.signal.lfilter([1 - filterCoeff, 0], [1, -filterCoeff], np.square(signalToFilter - mlTemp))

    ml = np.delete(mlTemp, np.arange(padLen))
    vl = np.delete(vlTemp, np.arange(padLen))

    sl = ml + startCoeff * np.sqrt(vl)
    Ni = len(rawSignal)
    points = np.array(np.where(rawSignal >= sl)[0])
    to_pop = np.array([])
    for i in range(1, len(points)):
        if points[i] - points[i - 1] == 1:
            to_pop = np.append(to_pop, i)
    to_pop = np.int64(to_pop)
    points = np.unique(np.delete(points, to_pop))
    NumberOfEvents = 0
    RoughEventLocations = np.zeros((10000, 3))
    event_current = np.zeros((10000, 3))

    for i in points:
        event_start_mean = ml[i-100]
        if i >= Ni - 10:
            break;
        start = i
        El = ml[i] + endCoeff * np.sqrt(vl[i])
        while rawSignal[i + 1] > El and i <= Ni - 10:
            i = i + 1
        if ((minDuration * sampleRate / 1000) < (i + 1 - start)) and ((i + 1 - start) < (maxDuration * sampleRate / 1000)) and (max(rawSignal[start:i + 1]) - event_start_mean) > 0:
            NumberOfEvents = NumberOfEvents + 1
            RoughEventLocations[NumberOfEvents - 1, 2] = i + 1 - start
            RoughEventLocations[NumberOfEvents - 1, 0] = start
            RoughEventLocations[NumberOfEvents - 1, 1] = i + 1
            event_current[NumberOfEvents - 1, 0] = (max(rawSignal[start:i + 1]) - event_start_mean)
            event_current[NumberOfEvents - 1, 1] = event_start_mean
            event_current[NumberOfEvents - 1, 2] = abs(
                event_current[NumberOfEvents - 1, 0] / event_current[NumberOfEvents - 1, 1]) * 10000

    event_statistic = np.zeros((NumberOfEvents, 6))
    event_statistic[:, 0] = RoughEventLocations[0: NumberOfEvents, 2] / sampleRate * 1000
    event_statistic[:, 1:4] = event_current[0: NumberOfEvents, 0:3]
    if iterNumber == 0:
        event_statistic[:, 4] = (RoughEventLocations[0: NumberOfEvents, 0] + iterNumber * sampleRate * 10) * 1000 / sampleRate
    else:
        event_statistic[:, 4] = (RoughEventLocations[0: NumberOfEvents,
                                 0] + iterNumber * sampleRate * 10) * 1000 / sampleRate -10
    event_statistic[:, 5] = fileNumber
    with open(fileName, "a+") as fp:
        np.savetxt(fp, event_statistic, fmt='%.3f', delimiter="\t")

