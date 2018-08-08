from random import shuffle, random, uniform, randint
from constants import *
import json
from math import cos, sin
import os
import numpy as np
'''parametros
cross sim nao
sinal aberto fechado
mc vel baixa media alta
carro atras sim nao
4 posicoes frente 7 possibilidades
4 posicoes lateral 8 possibilidades
carro na lateral sim nao indo vindo

fazer pro outro lado e mudar mc road
'''
#group in the middle of the road
middleGroup = []
for p1 in range(8):
	for p2 in range(8):
		for p3 in range(8):
			for p4 in range(8):
				middleGroup.append([p1, p2, p3, p4])

#remove identical situations
aux = [sorted(s) for s in middleGroup]

aux2 = []
for a in aux:
	if a not in aux2:
		aux2.append(a)
for a in aux2:
	shuffle(a)
middleGroup = aux2
middleGroup.pop(0)

#group by the side of the road
sideGroup = []
for p1 in range(9):
	for p2 in range(9):
		for p3 in range(9):
			for p4 in range(9):
				sideGroup.append([p1, p2, p3, p4])

#remove identical situations
aux = [sorted(s) for s in sideGroup]

aux2 = []
for a in aux:
	if a not in aux2:
		aux2.append(a)
for a in aux2:
	shuffle(a)
sideGroup = aux2

#road
#main car always in the first lane  / two way street
#road = [car behind(y/n), car on the side (y/n)(going or comming), crosswalk(y/n), semaphore(on/off), dist(0, 1), vel(0, 1, 2)]
road = []
for cb in range(2):
	for cs in range(2):
		for csgc in range(2):
			for cross in range(2):
				for s in range(2):
					for dist in range(2):
						for vel in range(3):
							if ((cs == 0 and csgc == 1) or (cross == 0 and s == 1)):
								pass
							else:
								road.append([cb, cs, 1 - 2*csgc, cross, s, dist, vel])

situations = []

for mg in middleGroup:
	for sg in sideGroup:
		for r in road:
			situations.append([mg, sg, r])


np.save('fixedSituations.npy', situations)
