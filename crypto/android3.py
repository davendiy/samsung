#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 06.02.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

secretKey = [0x69, 0xa7, 0x55, 0xf3, 3, 0x60, 0x4f, 0xa6, 0xb5, 0x35, 0xc3, 0xe0, 0x89, 0x46]
additionArray = [0xAD, 0x3A, 0x12, 0x90, 0x19, 0x99, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def xor(a, b):
    return a ^ b


def neg(a):
    b = bin(a)[2:]
    b = '0'*(8 - len(b)) + b
    res = ''
    for char in b:
        res += '0' if char == '1' else '1'
    return int(res, 2)


def func1(a1, a2):
    tmp = (-a2 & 7) % 256
    tmp = a1 >> tmp % 256
    tmp = tmp | ((a1 << a2) % 256)
    # return (a1 >> (-a2 & 7)) | (a1 << a2)
    return tmp % 256


def func2(a1, a2):
    return func1(a1, 8 - a2)


def bigFunction(userFlag, changedUserFlag):
    tmpUser = userFlag
    tmpChanged = changedUserFlag
    for i in range(len(userFlag)):
        tmpChanged[i] = func2(neg(xor(func1(tmpUser[i], 4), additionArray[i % 6])), 7)
    changedUserFlag = tmpChanged


def additionFunc(el, i):
    tmp1 = func1(el, 4)
    tmp1 = xor(tmp1, additionArray[i % 6])
    tmp1 = neg(tmp1)
    return func2(tmp1, 7)


def inverseFunc(sec_el, i):
    tmp = bin(sec_el)[2:]
    tmp = '0' * (8 - len(tmp)) + tmp
    tmp = tmp[-1] + tmp[:-1]
    tmp = neg(int(tmp, 2))
    tmp = xor(tmp, additionArray[i % 6])
    tmp = bin(tmp)[2:]
    tmp = '0' * (8 - len(tmp)) + tmp
    tmp = tmp[4:] + tmp[:4]
    return int(tmp, 2)


res = []
for i, el in enumerate(secretKey):
    tmp2 = inverseFunc(el, i)
    print(tmp2, el, i)
    res.append(tmp2)
print(res)
print(bytes(res))
#
# res = []
# for el_k in range(len(secretKey)):
#
#     for byte in range(2000):
#         tmp = additionFunc(byte, el_k)
#         if tmp == secretKey[el_k]:
#             res.append(tmp)
#             break
#     else:
#         res.append(0)

# print(bytes(res))
# print(res)
