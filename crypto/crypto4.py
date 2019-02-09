#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 29.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from collections import Counter
from itertools import product
import string

FREQUENCIES = {'a': 11.682,
               'b': 4.434,
               'c': 5.238,
               'd': 3.174,
               'e': 2.799,
               'f': 4.027,
               'g': 1.642,
               'h': 4.200,
               'i': 7.294,
               'j': 0.511,
               'k': 0.456,
               'l': 2.415,
               'm': 3.826,
               'n': 2.284,
               'o': 7.631,
               'p': 4.319,
               'q': 0.222,
               'r': 2.826,
               's': 6.686,
               't': 15.978,
               'u': 1.183,
               'v': 0.824,
               'w': 5.497,
               'x': 0.045,
               'y': 0.763,
               'z': 0.045}


def decrypt(iter, key):
    res = []
    n1 = len(iter)
    n2 = len(key)
    xkey = key * ((n1 // n2) + 1)
    for el, tmp_key in zip(iter, xkey):
        res.append((el + tmp_key) % 255)
    return res


def index_sames(iter):
    tmp_n = len(iter)
    counter = Counter(iter)
    return sum([val * (val - 1) / (tmp_n * (tmp_n - 1)) for val in counter.values()])


# with open('encrypted1.txt', 'rb') as file:
#     ciphertext = file.read()
#     for i in range(1, len(ciphertext)+1):
#         tmp_cipher = []
#         for j, el in enumerate(ciphertext):
#             if (j+1) % i == 0:
#                 tmp_cipher.append(el)
#         index = index_sames(tmp_cipher)
#         if abs(index - 0.065) <= 0.001:
#             print('i = {}, index = {}'.format(i, index))
#
# a = []
# with open('encrypted1.txt', 'rb') as file:
#     ciphertext = file.read()
#     for el in product(string.ascii_uppercase, repeat=6):
#         print(el)
#         tmp = decrypt(ciphertext, list(map(lambda a: int.from_bytes(bytes(a, encoding='utf-8'), byteorder='big'), el)))
#         a.append((list(filter(lambda a: 65 <= a <= 90 or 97 <= a <= 122, tmp))))
# print('decrypted, start sorting')
# a.sort(key=len)
#
# for row in a:
#     print(bytes(row))

with open('encrypted1.txt', 'rb') as file:
    ciphertext= file.read()

# 0
with open('tmp_result2.txt', 'wb') as file:
    for i in range(1, len(ciphertext), 6):
        file.write(bytes([ciphertext[i]]))
