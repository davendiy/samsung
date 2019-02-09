#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 05.02.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

func_indexes = [3, 6, 4, 3, 1, 2, 7, 6, 6, 7, 6, 2, 2, 4, 0, 0, 4, 0, 4, 7, 2, 7, 1]

output = [0x0D,
          0x99,
          0xEB,
          0x3A,
          0xFD,
          0x5F,
          0x76,
          0x3B,
          0x98,
          0x63,
          0x3A,
          0x19,
          0x2C,
          0x8D,
          0xCB,
          0xD9,
          0x8,
          0xCF,
          0xD,
          0xA4,
          0x2,
          0xA2,
          0xC0]


funcs = [lambda al: (al - 0x6C),
         lambda al: (al + 0x75),
         lambda al: al ^ 0x6C,
         lambda al: al ^ 0x7a,
         lambda al: rotate_right(al, 5),
         lambda al: rotate_left(al, 3),
         lambda al: rotate_right(al, 7),
         lambda al: (_not(al) - 0x2a) % 2 ** 32]


def rotate_left(al, i):
    tmp = bin(al).strip('0b')
    tmp = '0' * (8 - len(tmp)) + tmp
    for j in range(i):
        tmp = tmp[1:] + tmp[0]
    return int(tmp, 2)


def rotate_right(al, i):
    tmp = bin(al).strip('0b')
    tmp = '0' * (8 - len(tmp)) + tmp
    for j in range(i):
        tmp = tmp[-1] + tmp[:-1]
    return int(tmp, 2)


def _not(al):
    tmp = bin(al).strip('0b')
    tmp = '0' * (8 - len(tmp)) + tmp
    res = ''
    for el in tmp:
        res += '0' if el == '1' else '1'
    return int(res, 2)


res = [0 for _ in range(23)]
for k in range(23):
    res[k] = funcs[func_indexes[k]](output[k]) % 256

print(res)
print(bytes(res))
