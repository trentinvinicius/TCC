from random import shuffle, random, uniform, randint
from constants import *
import json
from math import cos, sin
import os
import numpy as np

def loadSituations():
	global loadedSituations
	loadedSituations = np.load('fixedSituations.npy')
	shuffle(loadedSituations)

def roadSides(laneMain, numLanes):
	if (laneMain <= numLanes/2.0):
	    zPos = -(numLanes/2.0 - laneMain + 0.5) * ROADSIZE
	else:
	    zPos = (laneMain - numLanes/2 -1 + 0.5) * ROADSIZE
	return (zPos + numLanes/2 * ROADSIZE, zPos - numLanes/2 * ROADSIZE)

def createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, name, visualization, test, parameters = [0, 0, 0, 0, 0]):
	msg = {"mainCarInfo": mainCarInfo, "roadInfo": roadInfo, "peopleInfo": peopleInfo, "otherCarsInfo": otherCarsInfo, "treepoleInfo": treepoleInfo, \
		   "animalInfo": animalInfo, "parameters": parameters, "name": name, "test" : test, "visualization" : visualization}
	return json.JSONEncoder().encode(msg)
	
def getSituations(num):
	loadSituations()
	vec = []
	situations = []
	l = len(loadedSituations)
	u = 0
	while u < num:
		r = randint(0, l)
		while r in vec:
			r = randint(0, l)
		vec.append(r)
		s = loadedSituations[r]
		result = True
		n = 0
		while (result and n < 5):
			tempoGeral = []
			mg, sg, road = s
			#print "MG: ", mg, " SG: ", sg
			velocity = (road[5]*10 + 10) + uniform(-5, 5)

			mainCarInfo = (int(5*random()), velocity, 0)
			if road[1] == 1:
				direction = 0
			else:
				direction = 1
			peopleMiddlePos = road[5]*20 + 20 + uniform(-10, 10)  #DEIXAR SOMENTE UNIFORM
			if road[3] == 1:
				crossPos = peopleMiddlePos
			else:
				crossPos = 0.0
			numLanes = 2 + randint(0,1) * 2
			laneMain = 1 + int(randint(0,1)*numLanes/4)
			roadInfo = [numLanes, direction, laneMain, crossPos, road[4]]
			
			otherCarsInfo = []
			peopleInfo = []
			treepoleInfo = []
			animalInfo = []

			if (road[0] == 1):
				otherCarsInfo.append([(-25 + uniform(-15, 15), 0, 0), 1, velocity, 0])
			if (road[1] == 1):
				if road[2] == -1:
					aux = 25
					if numLanes == 2:
						zCar = - 3.0
					else:
						if laneMain == 1: 
							zCar = - 6.0
						else:
							zCar = - 3.0
				else:
					aux = -25
					zCar = - 3.0
				otherCarsInfo.append([(aux + uniform(-15, 15), 0, zCar), road[2], velocity, 1])
			
			zs = []
			for i, pos in enumerate(mg):
				xPos = i%2 + peopleMiddlePos - 0.5
				zPos = uniform(-1.5, 3.5)
				maxVelocity = 1.0
				v = uniform(0, maxVelocity)
				for j, vel, z in zs:
					if j == i%2:
						while abs(z - zPos) < 1:  #check if two components are sharing the same space
							zPos = uniform(-1.5, 3.5)
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
			
			sidePos = roadSides(laneMain, numLanes)[0]
			xs = []
			if road[2] == 1:
				xs.append((0, peopleMiddlePos - 1.5))
			for i, pos in enumerate(sg):
				xPos = uniform(peopleMiddlePos - 5, peopleMiddlePos - 2)
				if pos == 8:
					k = 0 # treepole can only be in the first lane
				else:
					k = i
				zPos = k%2 + 1.5 + sidePos
				for j, x in xs:
					if j == k%2:
						while abs(x - xPos) < 0.8:  #check if two components are sharing the same space
							xPos = uniform(peopleMiddlePos - 5, peopleMiddlePos - 2)
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
					if road[3] == 1:
						pass
					else:
						treepoleInfo.append([xPos, 0, randint(0,1), i])

				for x in range(-10, 200, 10):
					treepoleInfo.append([x, 1, 1, x + 10])
					
			jsonParameters = createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, 'Test', False, True)
			with open(FILEWRITE, 'w') as outfile:
				json.dump(jsonParameters, outfile)
			os.system('python callSim.py')
			with open(FILEREAD) as data:
				jsonResult = json.load(data)

			result = json.JSONDecoder().decode(jsonResult)
			#print "RESULTADO: ", result
			n += 1
			if result != True:
				simOK = True
				result = False
			else:
				simOK = False

		if simOK:
			situations.append([mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo])
			u += 1

		if u % 100 == 0:
			print u
			'''
			print "SIM OK"
			jsonParameters = createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, animalInfo, 'Test', True, False)
			with open(FILEWRITE, 'w') as outfile:
				json.dump(jsonParameters, outfile)
			os.system('python callSim.py')
			with open(FILEREAD) as data:
				jsonResult = json.load(data)

			result = json.JSONDecoder().decode(jsonResult)
			print "RESULTADO: ", result'''
	return situations
