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
          0x0FD,
          0x5F,
          0x76,
          0x3B,
          0x98,
          0x63,
          0x3A,
          0x19,
          0x2C,
          0x8D,
          0x0CB,
          0x0D9,
          0x8,
          0x0CF,
          0x0D,
          0x0A4,
          0x2,
          0x0A2,
          0x0C0]


funcs = [lambda al: (al + 0x6C),
         lambda al: (al - 0x75),
         lambda al: al ^ 0x6C,
         lambda al: al ^ 0x7A,
         lambda al: rol(al, 5, 8),
         lambda al: ror(al, 3, 8),
         lambda al: rol(al, 7, 8),
         lambda al: _not(al + 0x2A)]


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


rol = lambda val, r_bits, max_bits: \
    (val << r_bits % max_bits) & (2 ** max_bits - 1) | \
    ((val & (2 ** max_bits - 1)) >> (max_bits - (r_bits % max_bits)))

# Rotate right: 0b1001 --> 0b1100
ror = lambda val, r_bits, max_bits: \
    ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))


res = []
for k in range(23):
    for el in range(1, 255):

        if funcs[func_indexes[k]](el) % 256 == output[k]:
            res.append(el)
            break
    else:
        res.append(32)


print(res)
print(bytes(res))
