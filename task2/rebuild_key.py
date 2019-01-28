#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 25.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

"""
Find the key of AES-128 doing the CPA attack on the last round of cryptographic protocol.
This program rebuilds the main key of AES-128 from the 10-th round key founded by the main program.
"""

import numpy as np
from Crypto.Cipher import AES
from AES_constants import Sbox, rConstants

texts_in = np.load('textin.npy')
texts_out = np.load('textout.npy')

NROUNDS = 11  # amount of rounds
N = 4         # amount of 4-bytes blocks in key


def rot_word(array: list):
    """ Standard RotWord function in AES.

    change array [1, 2, 3, 4] -> [2, 3, 4, 1]
    :param array: python list
    :return: changed python list
    """
    return array[1:] + [array[0]]


def xor(array1, array2):
    """ Vectorized exclusive OR.

    :param array1: first vector (iterable)
    :param array2: second vector (iterable)
    :return: vector with coordinates that are XOR of the relevant
    coordinates of array1 and array2
    """
    return np.array(list(map(lambda a, b: a ^ b, array1, array2)))


def inv_key_schedule(last_key: np.ndarray):
    """ Compute the main key of AES using key of the last round (10-th)

    This is inverse variation of AES piece named 'Key Expansion'
    :param last_key: array of numbers from 0 to 255
    :return: array of numbers from 0 to 255
    """
    w = np.zeros((N * NROUNDS, 4), int)             # array of 4-bytes blocks (every N bytes is the one round key)
    w[N * NROUNDS - N:] = last_key.reshape(N, 4)    # The last N blocks is the last key
    res_key = np.zeros((N, 4), int)                 # The first N blocks is the main key
    for i in range(N * NROUNDS - 1, -1, -1):
        if i < N:                      # just algorithm from wikipedia where w_i and w_i-N are swapped
            res_key[i] = w[i]
        elif i >= N and i % N == 0:
            w[i - N] = w[i] ^ rot_word(list(Sbox[w[i - 1]])) ^ rConstants[i // N]
        elif i >= N > 6 and i % N == 4:
            w[i - N] = w[i] ^ Sbox[w[i - 1]]
        else:
            w[i - N] = w[i - 1] ^ w[i]

    for i, row in enumerate(w):   # for debugging print all the round keys
        if i % 4 == 0:
            print()
        print(row)

    return list(res_key.reshape(1, N * 4)[0])


if __name__ == '__main__':
    test_key = np.array([160, 18, 2, 26, 245, 5, 43, 216, 26, 128, 193, 217, 6, 28, 217, 240])
    key = inv_key_schedule(test_key)

    print('key:', bytes(key))
    test_cipher = AES.new(bytes(key), AES.MODE_ECB)  # mode for AES - electronic codebook
    print('plaintext:', bytes(list(texts_in[0])))
    print('ciphertext in files:       ', bytes(list(texts_out[0])))
    print('ciphertext using found key:', test_cipher.encrypt(bytes(list(texts_in[0]))))
