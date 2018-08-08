from random import shuffle, random, uniform, randint
from constants import *
import json
import pickle
from math import cos, sin
import os
import numpy as np

def roadSides(laneMain, numLanes):
	if (laneMain <= numLanes/2.0):
	    zPos = -(numLanes/2.0 - laneMain + 0.5) * ROADSIZE
	else:
	    zPos = (laneMain - numLanes/2 -1 + 0.5) * ROADSIZE
	return (zPos + numLanes/2 * ROADSIZE, zPos - numLanes/2 * ROADSIZE)

def createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, riverInfo, name, visualization, test, parameters = [0, 0, 0, 0, 0]):
	msg = {"mainCarInfo": mainCarInfo, "roadInfo": roadInfo, "peopleInfo": peopleInfo, "otherCarsInfo": otherCarsInfo, "treepoleInfo": treepoleInfo, \
		   "animalInfo": animalInfo, "riverInfo": riverInfo, "parameters": parameters, "name": name, "test" : test, "visualization" : visualization}
	return json.JSONEncoder().encode(msg)

def getSituations(num, percent):
	"Load the situations based on the percentual from each type"
	global loadedSituations
	options = ['kidsmoreDifficult', 'kidslessDifficult', 'adultsmoreDifficult', 'adultslessDifficult', 'elderlymoreDifficult', 'elderlylessDifficult', 'femalemoreDifficult', \
	           'femalelessDifficult', 'malemoreDifficult', 'malelessDifficult', 'animallessDifficult', 'animalmoreDifficult', 'generalmoreDifficult', 'generallessDifficult']
	totalSimulations = []
	for i, file in enumerate(options):
		size = int(percent[i]*num)
		if size > 0:
			filename = "/home/vinicius/Situations/" + file
			with open(filename, 'rb') as inputFile:
				load = pickle.load(inputFile)
			shuffle(load)
			l = len(load)
			situations, vec = [], []
			u = 0
			if size > len(load):
				size = len(load)
			while (u < size):
				r = randint(0, l)
				while r in vec:
					r = randint(0, l)
				vec.append(r)
				situation = trySituation(load[r])
				if not situation == -1:
					situations.append(situation)
					u += 1
			for s in situations:
				totalSimulations.append(s)
	return totalSimulations

def trySituation(situation):
	result = True
	n = 0
	aux = randint(0,1)
	if aux == 1:
		river = True
	else:
		river = False
		riverPos = 0
	# try 5 times to create a situation
	while (result and n < 5):
		mg, sg, road = situation
		# mainCar
		velocity = uniform(MINVELOCITY, MAXVELOCITY)
		numPassengers = randint(1, 2)
		mainCarInfo = (numPassengers, velocity, 0)

		# position where the people will be placed
		peoplePosition = uniform(MINCROSSPOS, MAXCROSSPOS)

		tree, cross, numLanes, mainCarLane, carRight, carBehind, carLeft = road

		# road (numLanes, direction, position mainCar, crosswalk position, status semaphore)
		if (carLeft <= 2 and numLanes%2 == 0 and mainCarLane != numLanes):
			direction = 1
		else:
			direction = 0
		if cross > 0:
			crossPos = peoplePosition
			if river:
				riverPos = peoplePosition + 5 + RIVERSIZE/2
			if cross == 2:
				statusSemaphore = 1
			else:
				statusSemaphore = 0
		else:
			if river:
				riverPos = peoplePosition
			crossPos = 0
			statusSemaphore = 0

		riverInfo = [river, riverPos]


		roadInfo = (numLanes, direction, mainCarLane, crossPos, statusSemaphore)

		# treepole [(x, z, tree, num)]
		treepoleInfo = [] 
		if (tree == 1):
			for j in range(16):
				posX = -10 + 10*j
				if riverInfo[0]:
					if riverInfo[1] - RIVERSIZE/2 < posX < riverInfo[1] + RIVERSIZE/2:
						continue
				treepoleInfo.append([posX, 0, 1 if j%2 == 0 else 0, j])
				treepoleInfo.append([posX, 1, 1 if j%2 == 0 else 0, 16 + j])

		#otherCars [(position, direction, velocity, num)]
		otherCarsInfo = []
		if carBehind:
			otherCarsInfo.append([(-uniform(10, MAXDISTOTHERCAR/2), 0, 0), 1, velocity, 0])
		# car on the left side = [none, comming stopped, comming running, going stopped, going running]
		if mainCarLane == 1 and numLanes == 4: # decide where the car on the left will be placed
			z1Pos = -6.0
			z2Pos = -9.0
		else:
			z1Pos = -3.0
			z2Pos = -6.0
		#print carLeft
		if 0 < carLeft < 3: 
			otherCarsInfo.append([(uniform(peoplePosition, MAXDISTOTHERCAR) if carLeft % 2 == 0 else peoplePosition + 4.0, 0, z1Pos), -1, velocity if carLeft % 2 == 0 else 0, 1])
			if numLanes == 4: # add a car on the forth lane
				otherCarsInfo.append([(uniform(peoplePosition, MAXDISTOTHERCAR) if carLeft % 2 == 0 else peoplePosition + 4.0, 0, z2Pos), -1, velocity if carLeft % 2 == 0 else 0, 1])
		elif carLeft > 2:
			otherCarsInfo.append([(-uniform(10, MAXDISTOTHERCAR/2) if carLeft % 2 == 0 else peoplePosition - 4.0, 0, z1Pos), 1, velocity if carLeft % 2 == 0 else 0, 1])			
			if numLanes == 4: # add a car on the forth lane
				otherCarsInfo.append([(-uniform(10, MAXDISTOTHERCAR/2) if carLeft % 2 == 0 else peoplePosition - 4.0, 0, z2Pos), 1, velocity if carLeft % 2 == 0 else 0, 1])			
		# car on the right side = [none, stopped, running]
		if carRight:
			otherCarsInfo.append([(-uniform(10, MAXDISTOTHERCAR/2) if carRight % 2 == 0 else peoplePosition - 4.0, 0, 3.0), 1, velocity if carRight % 2 == 0 else 0, 2])			
		# people [(position, velocity, gender, age, num)]
		peopleInfo = []
		# animal [(position, velocity, num)]
		animalInfo = []

		# mainGroup		
		zs = []
		for i, pos in enumerate(mg):
			xPos = i%2 + peoplePosition - 0.5
			zPos = uniform(-0.5, 3.5)
			maxVelocity = 1.0
			v = uniform(0, maxVelocity)
			for j, vel, z in zs:
				if j == i%2:
					while abs(z - zPos) < 1:  #check if two components are sharing the same space
						zPos = uniform(-0.5, 3.5) # mainCar is always in 0.0
					v = vel
			zs.append((i, v, zPos))
			o = uniform(83,97)
			
			if (pos == 0):
				pass
			elif (pos == 1):
				peopleInfo.append([(xPos, 0, zPos), v, o, 0, 0, i])
			elif (pos == 2):
				peopleInfo.append([(xPos, 0, zPos), v, o, 0, 1, i])
			elif (pos == 3):
				peopleInfo.append([(xPos, 0, zPos), v, o, 0, 2, i])
			elif (pos == 4):
				peopleInfo.append([(xPos, 0, zPos), v, o, 1, 0, i])
			elif (pos == 5):
				peopleInfo.append([(xPos, 0, zPos), v, o, 1, 1, i])
			elif (pos == 6):
				peopleInfo.append([(xPos, 0, zPos), v, o, 1, 2, i])
			else:
				animalInfo.append([(xPos, 0, zPos), v, o, i])
		
		# sideGroup
		sidePos = roadSides(mainCarLane, numLanes)[0]
		xs = []
		if cross: # add the pole from the semaphore
			xs.append((0, peoplePosition - 1.5))
		if sg != None:
			for i, pos in enumerate(sg):
				xPos = uniform(peoplePosition - 5, peoplePosition - 2)
				if pos == 8:
					k = 0 # treepole can only be in the first lane
				else:
					k = i
				zPos = k%2 + 1.5 + sidePos
				for j, x in xs:
					if j == k%2:
						while abs(x - xPos) < 0.8:  #check if two components are sharing the same space
							xPos = uniform(peoplePosition - 5, peoplePosition - 2)
				xs.append((k, xPos))
				o = uniform(83,97)
				v = 0

				if (pos == 0):
					pass
				elif (pos == 1):
					peopleInfo.append([(xPos, 0, zPos), v, o, 0, 0, i + 7])
				elif (pos == 2):
					peopleInfo.append([(xPos, 0, zPos), v, o, 0, 1, i + 7])
				elif (pos == 3):
					peopleInfo.append([(xPos, 0, zPos), v, o, 0, 2, i + 7])
				elif (pos == 4):
					peopleInfo.append([(xPos, 0, zPos), v, o, 1, 0, i + 7])
				elif (pos == 5):
					peopleInfo.append([(xPos, 0, zPos), v, o, 1, 1, i + 7])
				elif (pos == 6):
					peopleInfo.append([(xPos, 0, zPos), v, o, 1, 2, i + 7])
				elif (pos == 7):
					animalInfo.append([(xPos, 0, zPos), v, o, i])
				else:
					treepoleInfo.append([xPos, 0, 1, i])
	
		jsonParameters = createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, riverInfo, 'Test', False, True)
		with open(FILEWRITE, 'w') as outfile:
			json.dump(jsonParameters, outfile)
		os.system('python callSim.py')
		with open(FILEREAD) as data:
			jsonResult = json.load(data)
		result = json.JSONDecoder().decode(jsonResult)

		#print "RESULTADO: ", result
		n += 1
		"If True an unexpected collision has occured"
		if result != True:
			jsonParameters = createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, riverInfo, 'Test', False, False, parameters = [MAXBRAKEFORCE, 0, 0, 0, 0])
			with open(FILEWRITE, 'w') as outfile:
				json.dump(jsonParameters, outfile)
			os.system('python callSim.py')
			with open(FILEREAD) as data:
				jsonResult = json.load(data)
			result = json.JSONDecoder().decode(jsonResult)
			collisions, inRiver, out, minDist = result
			#print collisions
			if len(collisions) < 1:
				simOK = False
			else:
				simOK = False
				#result = False
				for c in collisions:
					if "Person" in c['geomName'] or "Animal" in c['geomName']:
						simOK = True
						result = False
						break
			#simOK = True
			#result = False
		else:
			simOK = False

	if simOK:
		return [mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo, riverInfo]
	else:
		return -1