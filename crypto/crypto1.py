#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 29.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from string import ascii_lowercase


def caesar_cipher(text, n):
    return ''.join(map(lambda a: ascii_lowercase[(ascii_lowercase.find(a) + n) % len(ascii_lowercase)], text))


if __name__ == '__main__':
    string = input('string: ').lower()
    test_n = int(input('n: '))
    print('res:', caesar_cipher(string, test_n))
