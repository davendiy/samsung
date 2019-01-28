#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 26.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import numpy as np
import matplotlib.pyplot as plt
from AES_constants import Sbox


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
    # cov = sum([(x[_i] - meanX) * (y[_i] - meanY) for _i in range(len(x))])
    cov = sum(x*y)
    # meanQuadraticX = sum([(x[_i] - meanX) ** 2 for _i in range(len(x))]) ** 0.5
    meanQuadraticX = sum(x ** 2)
    # meanQuadraticY = sum([(y[_i] - meanY) ** 2 for _i in range(len(y))]) ** 0.5
    meanQuadraticY = sum(y ** 2)

    res = cov / np.sqrt(meanQuadraticX * meanQuadraticY)
    return abs(res)


def cross_all_bytes(texts_in, byte_num, n):
    """ Byte search function (iterator).
    For each byte from 0 to 255 builds array of leakages for all traces in the context of
    our math model (attack on the first round).

    :param texts_in: numpy array of cipher text
    :param byte_num: a number of the byte we search
    :param n: amount of traces
    :return: supposed byte (int number), array of leakages
    """
    for hyp in range(256):
        leak_array = np.zeros(n)
        for _i in range(n):
            # leak_array[_i] = hamming_weight(Sbox[texts_in[_i][byte_num]] ^ hyp)
            leak_array[_i] = hw[Sbox[texts_in[_i][byte_num] ^ hyp]]
        yield hyp, leak_array


def sad(x, y):
    """ Sum of absolute differences between 2 arrays.

    :param x: array 1
    :param y: array 2
    :return: array 3
    """
    return sum(abs((x-y)))


textIn = np.load('textin.npy')      # load the input data
textOut = np.load('textout.npy')
traces = np.load('traces.npy')

traces_amount = len(textIn)
meas_amount = len(traces[0])

plt.plot(traces[0], linewidth=0.2)   # plot the first trace in order to choose the parameters of the window
plt.show()

start_window = 800     # parameters of the pattern window that we will search on the other traces
end_window = 1200      # the optimal parameters were chosen by trial and error
len_window = end_window - start_window

start_range = 100      # range on the traces where we will search the pattern
end_range = 4000

diffs = [0, ]          # array with differences along the X-axis for each trace
for trace in traces[1:]:
    diff = 0
    min_sad = 10005000000000         # we search the place on each trace where the SAD is minimum

    for i in range(start_range, end_range):
        if i + len_window > end_range:     # if the window isn't in the chosen range - stop the search
            break
        tmp_sad = sad(traces[0][start_window:end_window], trace[i:i + len_window])
        if tmp_sad < min_sad:
            min_sad = tmp_sad
            diff = i - start_window    # difference along the X-axis between the start of the pattern window and
    diffs.append(diff)                 # start of the place, were we found same window

# the range on the traces that there is on each trace
start = abs(min(diffs))
end = meas_amount - max(diffs)

# plot all the traces to illustrate the alignment
for i in range(traces_amount):
    plt.plot(np.arange(start, end), traces[i][start+diffs[i]:end+diffs[i]], linewidth=0.2)
plt.show()

for i in range(20):
    plt.plot(np.arange(start, end), traces[i][start:end] + i, linewidth=0.2)
plt.show()

for i in range(20):
    plt.plot(np.arange(start, end), traces[i][start+diffs[i]:end+diffs[i]] + i, linewidth=0.2)
plt.show()
print(start, end)


key = []
# the part from the task 1
leak_places = []
for k in range(16):
    max_cor = 0
    best_byte = 0
    leak_place = 0
    for byte, leak in cross_all_bytes(textIn, k, traces_amount):

        for i in range(start, end):
            real_values = [traces[j][i+diffs[j]] for j in range(traces_amount)]
            tmp_cor = cor2(leak, real_values)
            # print(tmp_cor, cor2(leak, real_values))
            if tmp_cor > max_cor:
                max_cor = tmp_cor
                best_byte = byte
                leak_place = i
        print(byte)

    leak_places.append(leak_place)
    key.append(best_byte)
    print('\nbyte number:', k)

    print('best byte:', best_byte)
    print('max correlation:', max_cor)
    print('leak place:', leak_places[-1])

print(key)
print(leak_places)
