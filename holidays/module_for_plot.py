#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 21.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

""" Module with functions for plotting
"""

import matplotlib.pyplot as plt


# styles of lines
styles = ['-', '--', '-.', '_']

# colors of lines
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']


number_of_style = 0


def movespinesticks():
    """ Move axises to zero position
    """
    ax = plt.gca()  # get current object

    # do right and top axises invisible
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    # move bottom and left axises
    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data', 0))

    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data', 0))


def plot(x, y, string: str, show=True):
    """ Plot function graph with different color and style of line
    
    :param x: numpy array
    :param y: numpy array the same length with x
    :param string: label of graph
    :param show: optional parameter True if you want to show this graph on separated window, 
                 False means that graph won't be shown before calling plt.show() 
    """
    global number_of_style

    plt.xlabel('x')
    plt.ylabel('y')
    # style = styles[number_of_style % len(styles)] + colors[number_of_style % len(colors)]
    style = styles[0] + colors[number_of_style % len(colors)]
    number_of_style += 1
    plt.plot(x, y, style, linewidth=.5, label=string)
    plt.legend(loc='best')
    if show:
        plt.show()
