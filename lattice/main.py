#!/usr/bin/env python3
# -*-encoding: utf-8-*-

# created: 29.01.19
# by David Zashkolny
# 2 course, comp math
# Taras Shevchenko National University of Kyiv
# email: davendiy@gmail.com

from lattice.solve_module import *
import olll

modulo = 275492675921517885660715486088112770209
n = 40

a = []
for i in range(1, n+1):
    with open(f'messages/{i}', 'r') as file:
        tmp = list(map(int, file.readline().strip('>').split()))
        tmp2 = int(file.readline().strip('<'))
        a.append(tmp + [tmp2])

print(a)

res = solve(np.array(a), modulo)
res = olll.reduction(res[:-3], 0.75)

for row in res:
    print(list(row))
#
max_len = max(map(lambda a: len(str(a)), res[0]))
with open('output2.txt', 'w') as file:
    for row in res:
        file.write(' '.join(map(lambda a: str(a) + ' '*(max_len - len(str(a))), row)))
        file.write('\n')
