#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 22.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com


import numpy as np
import matplotlib.pyplot as plt
from AES_constants import Sbox


def hamming_weight(data):
    tmp = bin(data)
    return tmp.count('1')


hw = [bin(n).count("1") for n in range(0, 256)]


def cor(x, y):
    meanX = np.mean(x)
    meanY = np.mean(y)
    # x = x - meanX
    # y = y - meanY
    cov = sum([(x[_i] - meanX) * (y[_i] - meanY) for _i in range(len(x))])
    # cov = sum(x*y)
    meanQuadraticX = sum([(x[_i] - meanX) ** 2 for _i in range(len(x))]) ** 0.5
    # meanQuadraticX = sum(x ** 2)
    meanQuadraticY = sum([(y[_i] - meanY) ** 2 for _i in range(len(y))]) ** 0.5
    # meanQuadraticY = sum(y ** 2)

    res = cov / (meanQuadraticX * meanQuadraticY)
    return abs(res)


def cor2(x, y):
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
    for hyp in range(256):
        leak_array = np.zeros(n)
        for _i in range(n):
            # leak_array[_i] = hamming_weight(Sbox[texts_in[_i][byte_num]] ^ hyp)
            leak_array[_i] = hw[Sbox[texts_in[_i][byte_num] ^ hyp]]
        yield hyp, leak_array


textIn = np.load('/files/univer/samsung/task1/textin.npy')
traces_amount = len(textIn)

textOut = np.load('/files/univer/samsung/task1/textout.npy')
traces = np.load('/files/univer/samsung/task1/traces.npy')
tmp_traces = np.transpose(traces)

meas_amount = len(traces[0])

plt.plot(traces[0], linewidth=0.2)
plt.show()


key = []

leak_places = []
for k in range(16):
    max_cor = 0
    best_byte = 0
    leak_place = 0
    for byte, leak in cross_all_bytes(textIn, k, traces_amount):

        for i in range(meas_amount):
            real_values = tmp_traces[i]
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
