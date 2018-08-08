from random import shuffle, random, uniform, randint
from constants import *
import pickle
from math import cos, sin
import os
import numpy as np
from copy import deepcopy

"Create mainGroup and sideGroup"
'''
0 - nobody
1 - boy
2 - girl
3 - man
4 - woman
5 - old man
6 - old woman
7 - animal
8 - tree (must be only one)
'''
#based on the data above
kidsOptions = [0, 1, 2]
adultsOptions = [0, 3, 4]
elderlyOptions = [0, 5, 6]
maleOptions = [0, 1, 3, 5]
femaleOptions = [0, 2, 4, 6]
animalOptions = [0, 7]
generalOptions = [x for x in range(8)]

options = [kidsOptions, adultsOptions, elderlyOptions, maleOptions, femaleOptions, animalOptions, generalOptions]

mainGroup = []

print "Creating groups..."

for op in options:
	aux = []
	for p1 in op:
		for p2 in op:
			for p3 in op:
				for p4 in op:
					aux.append([p1, p2, p3, p4])
	#remove identical combinations
	aux2 = [sorted(s) for s in aux]
	aux3 = []
	for a in aux2:
		if a not in aux3:
			aux3.append(a)
	for a in aux3:
		shuffle(a) #change the positions on the vector.
	aux = aux3
	aux.pop(0) # remove [0, 0, 0, 0]
	mainGroup.append(aux)

sideGroup = deepcopy(mainGroup[6])
#add a tree
sideGroup.append(shuffle([0, 0, 0, 9]))


"Create the road configuration"
'''
trees on both sides (yes/no)
crossroad [none, signal open for cars, signal closed]
number of lanes (1, 2, 3, 4)
	if 4 both directions; 3 only one, 2 can be both
mainCar lane(1, 2)
	if 2:
		car on the right side = [none, stopped, running]
car behind (yes/no)
car on the left side = [none, comming stopped, comming running, going stopped, going running]

velocity and position will be uniformly distributed in a predefined range
'''
treeOptions = [0, 1]
crossOptions = [0, 1, 2]
numLanesOptions = [1, 2, 3, 4]
mainCarLaneOptions = [1, 2]
carRightSideOptions = [0, 1, 2]
carbehindOptions = [0, 1]
carLeftSideOptions = [0, 1, 2, 3, 4]

print "Creating road..."

road = []
for to in treeOptions:
	for co in crossOptions:
		for nlo in numLanesOptions:
			for mclo in mainCarLaneOptions:
				for crso in carRightSideOptions:
					for cbo in carbehindOptions:
						for clso in carLeftSideOptions:
							if (nlo == 1): # there is only one lane where the mainCar can be
								mclo = 1
							if (mclo == 1): # it's not possible to have a car on the right side
								crso = 0
							if (nlo == 3 and clso in [1, 2]): # 3 lanes is only one way
								clso = 0
							if (nlo == 2 and mclo == 2): # 2 lanes and mainCar on the second
								clso = 0
							if (nlo == 1):
								crso = 0
								clso = 0

							road.append([to, co, nlo, mclo, crso, cbo, clso])

#remove identical combinations
aux = []
for r in road:
	if not r in aux:
		aux.append(r)
road = aux

moreDifficult = {}
lessDifficult = {}
#create empty lists for the categories in the dictionary
for i in range(len(mainGroup)):
	moreDifficult[i] = []
	lessDifficult[i] = []

print "Creating combinations..."

for pos, group in enumerate(mainGroup):
	for g in group:
		for sg in sideGroup:
			for r in road:
				combination = [g, sg, r]
				if (r[0] == 1 and r[4] == 1 and r[5] == 1 and r[6] in [1, 3]):
					moreDifficult[pos].append(combination)
				else:
					lessDifficult[pos].append(combination)

print "... finished"
for i in range(len(mainGroup)):
	print "Pos: ", i, " length moreDifficult: ", len(moreDifficult[i]), " length lessDifficult: ", len(lessDifficult[i])
'''
Pos:  0  length moreDifficult:  41580  length lessDifficult:  2231460
Pos:  1  length moreDifficult:  41580  length lessDifficult:  2231460
Pos:  2  length moreDifficult:  41580  length lessDifficult:  2231460
Pos:  3  length moreDifficult:  100980  length lessDifficult:  5419260
Pos:  4  length moreDifficult:  100980  length lessDifficult:  5419260
Pos:  5  length moreDifficult:  11880  length lessDifficult:  637560
Pos:  6  length moreDifficult:  977130  length lessDifficult:  52439310
'''
names = ['kids', 'adults', 'elderly', 'male', 'female', 'animal', 'general']
print "Saving..."

for i, n in enumerate(names):
	filename1 = n + 'moreDifficult'
	filename2 = n + 'lessDifficult'
	with open(filename1, 'wb') as out:
		pickle.dump(moreDifficult[i], out)
	with open(filename2, 'wb') as out:
		pickle.dump(lessDifficult[i], out)
#situations = [moreDifficult, lessDifficult]
#with open("newFixedSituations.txt", "wb") as outputFile:
#	pickle.dump(situations, outputFile)
print "...done"
