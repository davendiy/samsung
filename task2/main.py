#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 22.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
Find the key of AES-128 doing the CPA attack on the last round of cryptographic protocol.
This program analyses the traces of power consumption and finds the 10-th round key.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from AES_constants import InvSbox

# Hamming weight for numbers from 0 to 255
hw = [bin(n).count("1") for n in range(0, 256)]


def cor2(x, y):
    """ Absolute value of Pearson Correlation Coefficient for 2 sets

    :param x: numpy array of values
    :param y: numpy array of values
    :return: float number from 0 to 1
    """
    meanX = np.mean(x)
    meanY = np.mean(y)
    x = x - meanX
    y = y - meanY
    cov = sum(x*y)
    meanQuadraticX = sum(x ** 2)
    meanQuadraticY = sum(y ** 2)
    res = cov / np.sqrt(meanQuadraticX * meanQuadraticY)
    return abs(res)


def cross_all_bytes(texts_out, byte_num, n):
    """ Byte search function (iterator).
    For each byte from 0 to 255 builds array of leakages for all traces in the context of
    our math model (attack on the last round).

    :param texts_out: numpy array of cipher text
    :param byte_num: a number of the byte we search
    :param n: amount of traces
    :return: supposed byte (int number), array of leakages
    """
    for hyp in range(256):
        leak_array = np.zeros(n)
        for _i in range(n):
            leak_array[_i] = hw[InvSbox[texts_out[_i][byte_num] ^ hyp]]
        yield hyp, leak_array


def clean(tr: np.ndarray, _b, _a):
    """ Cleaning function

    :param tr: array of traces
    :param _b: result of signal.butter
    :param _a: result of signal.butter
    :return: clear traces
    """
    for _i in range(len(tr)):
        tr[_i] = signal.lfilter(_b, _a, tr[_i])
    return tr


# load dataset
textIn = np.load('textin.npy')
textOut = np.load('textout.npy')
traces = np.load('traces.npy')

plt.plot(traces[0], linewidth=0.2, label='Input signal')
plt.legend(loc='best')
plt.show()
# clean traces using numpy functions
b, a = signal.butter(6, 0.65, btype='low')
traces = clean(traces, b, a)

plt.plot(traces[0], linewidth=0.2, label='Cleaned signal')
plt.legend(loc='best')
plt.show()

traces_amount = len(textIn)
meas_amount = len(traces[0])
tmp_traces = np.transpose(traces)    # addition transposed array of traces


key = []             # array of best bytes
leak_places = []     # array of the moments of time where the best bytes was found
max_cors = []

for k in range(16):
    max_cor = 0      # max correlation for each byte
    best_byte = 0    # the value of the best byte
    leak_place = 0   # moment of time where the best byte was found
    for byte, leak in cross_all_bytes(textOut, k, traces_amount):

        for i in range(meas_amount):           # for each byte we search the biggest correlation
            real_values = tmp_traces[i]        # array of real values of the power consumption
            tmp_cor = cor2(leak, real_values)  # leak - array of supposed values of the power consumption
            if tmp_cor > max_cor:
                max_cor = tmp_cor
                best_byte = byte
                leak_place = i
        print(byte)

    leak_places.append(leak_place)
    key.append(best_byte)
    max_cors.append(max_cor)
    print('\nbyte number:', k)                # print the information
    print('best byte:', best_byte)
    print('max correlation:', max_cor)
    print('leak place:', leak_places[-1])

print(key)
print(leak_places)
print(max_cors)


# write temporary results to the text file
with open('results.txt', 'a') as file:
    file.write(f'\n{key}\n{leak_places}\n{max_cors}')
