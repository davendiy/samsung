#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 21.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

import numpy as np
from holidays import module_for_plot as plt
from numpy.fft import fft, ifft      # fast Fourier transform and an inverse one
import random
# %matplotlib inline

A = 0               # start of the signal
B = 30              # end of the signal
N = 1000            # amount of points
ENOUGH = 100        # amount of first points that will show frequencies of signal decomposition without noise
# it was chosen by trial and error

funcs_amount = 3    # amount of the trigonometric functions
noises_amount = 4   # amount of the trigonometric functions with high frequency (noise)

NpFunctions = [(np.sin, 'sin'), (np.cos, 'cos')]     # list for the random choice trigonometric function


def random_func():
    """ Create random trigonometric function (sin or cos)
    """
    tmp_func, tmp_func_name = NpFunctions[random.randint(0, 100) % 2]  # choose type of function
    _a = random.randint(0, 60) / 4      # amplitude
    phi = random.uniform(0, 1.5)        # frequency (will be multiplied by 2pi)
    r = random.randint(0, 10)           # displacement

    # result function with random parameters
    def res_func(x):
        return _a * tmp_func(2 * np.pi * phi * x + r)

    # documentation is appearance of function
    res_func.__doc__ = '{:0.1f}{}(2pi * {:0.2f}x + {})'.format(_a, tmp_func_name, phi, r)

    return res_func


def random_noise():
    """ Create random trigonometric function with hight frequency (noise)
    """
    tmp_func, tmp_func_name = NpFunctions[random.randint(0, 100) % 2]  # choose type of function
    _a = random.uniform(0, 5)           # amolitude
    phi = random.uniform(5, 10)         # frequency (will be multiplied by 2pi)

    # result function with random parameters
    def res_func(x):
        return _a * tmp_func(2 * np.pi * x * phi)

    print('{:0.1f}{}(2pi * {:0.2f}x)'.format(_a, tmp_func_name, phi))
    return res_func


def cleaning(func: callable, a: float, b: float, n: int):
    """ Function that removes noise from signal using 
    discrete Fourier transform
    
    :param func: python vectorized function of single variable
    :param a: start of signal
    :param b: end of signal
    :param n: amount of points
    :return: numpy array of x-s and numpy array of result values of function
    """
    x = np.linspace(a, b, n)        # tabulating of function
    y = func(x)

    ft_y = fft(y)                   # Fourier transform
    plt.plot(x, y, 'input data')    # show input data and its transform
    plt.plot(x, abs(ft_y), "Fourier transform of data")

    # replace all the values after ENOUGH points with zeros (delete hight frequences)
    res = ifft(list(ft_y[:ENOUGH]) + list(np.zeros(n-ENOUGH)))  # and do inverse transform
    return x, res


if __name__ == '__main__':

    functions = []                        # list of random functions
    label = 'f(x) = '                     # result function (sum of all)
    for j in range(funcs_amount):
        tmp_function = random_func()      # generate given amount of random functions
        functions.append(tmp_function)
        label += tmp_function.__doc__ + ' + '

    print('generated function: {}'.format(label.strip(' + ')))
    print('\nnoises:')
    functions += [random_noise() for j in range(noises_amount)]   # generate given amount of noises


    def test_func(x):
        """ Result function with noise that is the sum of all the generated functions 

        :param x: float or numpy array
        """
        return sum(map(lambda f: f(x), functions))


    test_x, good_y = cleaning(test_func, A, B, N)    # cleaning


    def test_func2(x):
        """ Result function without noise that is the sum of all the generated functions
        
        :param x: float or numpy array
        """
        return sum(map(lambda f: f(x), functions[:funcs_amount]))


    plt.plot(test_x, good_y, 'cleaned data by fft')
    plt.plot(test_x, test_func2(test_x), 'right data without noise')

    for j in range(funcs_amount-1):
        tmp_function = functions[j]
        plt.plot(test_x, tmp_function(test_x), f'component {j}', show=False)

    plt.plot(test_x, functions[funcs_amount-1](test_x), f'component {funcs_amount-1}', show=True)
