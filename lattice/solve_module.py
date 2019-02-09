#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 29.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np


class SolveException(Exception):

    def __str__(self):
        return "Element isn't reversible"


def xgcd(a, b):
    """ Extended euclidean algorithm for gaussian integers
    """

    # it is standard realisation of euclidean algorithm
    if abs(b) > abs(a):
        a, b = b, a

    if not b:
        return 1, 0, a

    q, r = a // b, a % b
    y, x, g = xgcd(b, r)
    return x, y - q * x, g


def inverse(x, modulo):
    a, b, d = xgcd(x, modulo)
    if d != 1:
        raise SolveException
    return b


def solve(matrix: np.ndarray, modulo):
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            x, y, d = xgcd(matrix[i, i], matrix[j, i])
            r = matrix[j, i]
            s = -matrix[i, i]
            matrix[i], matrix[j] = np.array([[x, y], [r, s]]).dot(np.array([matrix[i], matrix[j]]))
            # print(matrix)
            matrix[i] %= modulo
            matrix[j] %= modulo
            # print(matrix)
            # print()
        try:
            inv_aii = inverse(matrix[i, i], modulo)
        except SolveException:
            print('matrix is degenerate')
            continue
            # return matrix

        matrix[i] = (matrix[i] * inv_aii) % modulo
        for j in range(i):
            matrix[j] = (matrix[j] - matrix[i] * matrix[j, i]) % modulo
    return matrix


if __name__ == '__main__':
    print(solve(np.array([[26, 3, 4], [9, 34, 1]]), 36))
