#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 26.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from Crypto.Cipher import AES
import numpy as np

textIn = np.load('textin.npy')
textOut = np.load('textout.npy')


key = [49, 105, 86, 101, 32, 89, 48, 117, 124, 50, 32, 68, 114, 51, 64, 77]
leak = [1589, 1766, 1942, 2118, 1630, 2324, 1982, 2157, 1670, 1846, 2022, 2198, 1710, 1886, 2062, 2238]

test_cipher = AES.new(bytes(key), AES.MODE_ECB)      # mode for AES - electronic codebook
print(bytes(key))
print('plaintext:', textIn[0])
print('ciphertext in files:       ', bytes(list(textOut[0])))
print('ciphertext using found key:', test_cipher.encrypt(bytes(list(textIn[0]))))
