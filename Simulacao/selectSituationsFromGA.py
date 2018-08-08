import os
import pickle
import json
from constants import *

try:
	with open('Situations/alreadySeen.txt') as data:
		alreadySeen = json.load(data)
except:
	alreadySeen = []

try:
	with open('Situations/randomSituations') as data:
		randomSituations = pickle.load(data)
except:
	randomSituations = []
files = os.listdir('Situations')


def run(allData):
	global randomSituations
	mC, r, oC, p, a, tp = allData
	msg = {"mainCarInfo": mC, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oC, "treepoleInfo": tp, \
		   "animalInfo": a, "parameters": [0, 0, 0, 0, 0], "name": "Teste", "test" : False, "visualization" : True}

	jsonSim = json.JSONEncoder().encode(msg)
	with open(FILEWRITE, 'w') as outfile:
		json.dump(jsonSim, outfile)	
	os.system('python callSim.py')
	#result = raw_input('Good situation? (y/n) : ')

	#just to get the best
	result = 'y'
	if result == 'y':
		randomSituations.append(msg)

for file in files:
	if "_" in file and file not in alreadySeen and "2" == file[0]:
		try:

			filename = 'Situations/' + file
			print 'New file: ', filename
			with open(filename, 'rb') as inputFile:
				population = pickle.load(inputFile)
			score = 0
			for i, individual in enumerate(population):
				print individual.msg
				if abs(individual.score - score) > 1000:
					print 'Situation', i
					print individual.msg
					try:
						individual.msg["test"] = False
						individual.msg["visualization"] = True
						mC = individual.mainCar()
						r = individual.road()
						oC = individual.otherCars(r[0], r[1], r[2])
						p = individual.people()
						a = individual.animal()
						tp = individual.treepole()
						allData = [mC, r, oC, p, a, tp]
						run(allData)
					except:
						try:
							mC = individual.mainCar()
							r = individual.road()
							oC = individual.otherCars(r[0], r[1], r[2])
							p = individual.people()
							a = individual.animal()
							tp = individual.treepole()
							allData = [mc, r, oC, p, a, tp]
							run(allData)
						except:
							print "DEU ERRRRROOORR"
							print individual
				score = individual.score
			alreadySeen.append(file)
			try:
				with open('Situations/alreadySeen.txt') as out:
					json.dump(alreadySeen, out)
				with open('Situations/randomSituations') as out:
					pickle.dump(randomSituations, out)
			except:
				pass
			
		except:
			pass