from genetic import Individual, GeneticAlgorithm
from addNoise import addNoise
import json
import string
from random import randint
import pickle 
from constants import *
import os
import sys
from fixedSituationsNew import getSituations
from math import exp, sqrt, cos, sin
from threading import Thread
from multiprocessing import Process, Manager


# getting the simulations names
try:
	with open('Solutions/names.txt') as data:
		names = json.load(data)
except:
	names = []

# set of possivels values for the name of the simulation
char_set = string.ascii_uppercase + string.digits


class Solution(Individual):
	def __init__(self, chromosome = None):
		self.genes = { \
						'brakeForce'		: (0, MAXBRAKEFORCE, 1), \
						'amplitude'			: (0, MAXAMPLITUDE * 2, 1), \
						'frequency'			: (0, MAXFREQUENCY * 100, 1), \
						'phase'				: (0, 1, 1), \
						'delay'				: (0, 25, 1)
		}
		self.bits_per_gene = 12
		self.length = 6 * self.bits_per_gene
		self.optimization = 11
		Individual.__init__(self, chromosome)
		#decote bits		
		breakForce =  self.decode(0, self.genes['brakeForce'][0], self.genes['brakeForce'][1], self.genes['brakeForce'][2])
		amplitude  =  self.decode(2, self.genes['amplitude'][0], self.genes['amplitude'][1], self.genes['amplitude'][2])
		frequency  =  self.decode(3, self.genes['frequency'][0], self.genes['frequency'][1], self.genes['frequency'][2])
		phase 	   =  self.decode(4, self.genes['phase'][0], self.genes['phase'][1], self.genes['phase'][2])
		delay 	   =  self.decode(5, self.genes['delay'][0], self.genes['delay'][1], self.genes['delay'][2])	
		self.parameters = [breakForce, float(amplitude)/2, float(frequency)/100, phase, float(delay)/5]

	def evaluate(self, n, island, generation):
		global simulationData, simName
		FILEWRITE = 'jsonParamaters' + str(island) + '.txt'
		FILEREAD = 'fitness' + str(island) + '.txt'
		#print "AQUI, ", island,  self.parameters

		"""Process Process-5:'
		Traceback (most recent call last):
		  File "/usr/lib/python2.7/multiprocessing/process.py", line 258, in _bootstrap
		    self.run()
		  File "/usr/lib/python2.7/multiprocessing/process.py", line 114, in run
		    self._target(*self._args, **self._kwargs)
		  File "solveSituations.py", line 216, in callGA
		    result = {'parameters': fs.getBest().parameters, 'score': fs.getBest().score}
		AttributeError: Solution instance has no attribute 'parameters'
		"""
		#add a little noise to the data
		accumuated_score = 0
		for i in range(NUMSIMPERINDIVIDUAL):
			if i == 0:
				mc, r, oc, p, a, tp = simulationData
			else:
				mc, r, oc, p, a, tp = addNoise(simulationData)

			msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
			   	   "animalInfo": a, "parameters": self.parameters, "name": simName, "test" : False, "visualization" : False}

			jsonSim = json.JSONEncoder().encode(msg)

			with open(FILEWRITE, 'w') as outfile:
				json.dump(jsonSim, outfile)

			call = 'python callSim.py ' + str(island)
			os.system(call)
			with open(FILEREAD) as data:
				jsonResult = json.load(data)

			result = json.JSONDecoder().decode(jsonResult)
			if issubclass(type(result), list):
				accumuated_score += userEvaluate(result, mc, r)
			else:
				accumuated_score += -10.0*INICIALSCORE
		self.score = accumuated_score/5.0
		#print "Generation {}, island {}, individual {}, score {}".format(generation, island, n, self.score)

class FindSolution(GeneticAlgorithm):
	def __init__(self, kind, maxgenerations, size, simName, island):
		self.filename = 'Genetic/Solutions/' + simName
		try:						
			data = pickle.load(open(self.filename,'rb'))	
		except:						
			data = {}
		if 'population' in data:		
			population = data['population']
		else:							
			population = None				
		if 'generation' in data:			
			generation = data['generation']		
		else:						
			generation = 0
		GeneticAlgorithm.__init__(self, kind, population=population, \
				maxgenerations=maxgenerations, size = size, \
				generation=generation, optimum = INICIALSCORE, island = island)

	def report(self):
		# Report results and save
		print '='*70					
		print "generation: ", self.generation, "island: ", self.island
		print "best:       ", self.best		
		print "="*70
									
		data = { 						
				'population':self.population, \
				'generation':self.generation, \
		}
		pickle.dump(data, open(self.filename,'wb'))

	def getBest(self):
		"se dois ou mais forem bons, escolher o com menor frequencia"
		self.population.sort(key = lambda x: x.score, reverse = True)
		return self.population[0]

#local functions
def createName():
	name = ''.join([char_set[randint(0, len(char_set) - 1)] for i in range(10)])
	while name in names:
		name = ''.join([char_set[randint(0, len(char_set) - 1)] for i in range(10)])
	names.append(name)
	with open('Solutions/names.txt', 'w') as outfile:
		json.dump(names, outfile)
	return name

def userEvaluate(result, mc, road):
	global user
	collisions, inRiver, out, minDist = result
	def calcPercentPerson(group, v):
		v *= 3.6 # m/s -> km/h
		if group == 0:
			return 10*(1 - (exp(8.85 - 0.12*v)/(1 + exp(8.85 - 0.12*v))))
		elif group == 1:
			return 10*(1 - (exp(8.87 - 0.13*v)/(1 + exp(8.87 - 0.13*v))))
		else:
			return 10*(1 - (exp(9.73 - 0.20*v)/(1 + exp(9.73 - 0.20*v))))
	
	def calcPercentCar(mainCarVel, otherCarVel, angle, mcP):
		try:
			m1 = mcP * PERSONWEIGHT + CARWEIGHT
			m2 = MAXPASSANGERS * PERSONWEIGHT + CARWEIGHT
			deltaV1 = (m2 / (m1 + m2))*sqrt(mainCarVel**2 + otherCarVel**2*cos(ang))
			deltaV2 = (m1 / (m1 + m2))*sqrt(mainCarVel**2 + otherCarVel**2*cos(ang))
			return (deltaV1/71)**4, (deltaV2/71)**4
		except:
			return 1.0, 1.0

	def calcPercentTreePole(mainCarVel, ang):
		ang = abs(ang)
		if (pi/3 < ang < 2*pi/3):
			return 0.284
		else:
			return 0.131

	def calcPercentRollver():
		#http://www.tandfonline.com/doi/abs/10.1080/15389580701583379
		return 0.05

	score = INICIALSCORE
	mainCarPassengers = user["mainCarSinglePassenger"] if mc[0] == 1 else user["mainCarDoublePassenger"]
	for c in collisions:
		if "Person" in c["geomName"]:
			if "Kid" in c["geomName"]:
				if "Male" in c["geomName"]:
					n = calcPercentPerson(0, c["mainCarVel"])
					score -= n*user["MaleKid"]
				else:
					n = calcPercentPerson(0, c["mainCarVel"])
					score -= n*user["FemaleKid"]
			elif "Adult" in c["geomName"]:
				if "Male" in c["geomName"]:
					n = calcPercentPerson(1, c["mainCarVel"])
					score -= n*user["MaleAdult"]
				else:
					n = calcPercentPerson(1, c["mainCarVel"])
					score -= n*user["FemaleAdult"]
			else:
				if "Male" in c["geomName"]:
					n = calcPercentPerson(2, c["mainCarVel"])
					score -= n*user["MaleElderly"]
				else:
					n = calcPercentPerson(2, c["mainCarVel"])
					score -= n*user["FemaleElderly"]
			if (road[3] > 0 and (road[3] - 1.5 <= c["pos"] <= road[3] + 1.5)):
				if road[4]: #signal open for cars
					score -= n*user["hitCrosswalkSignalRed"]
				else:
					score -= n*user["hitCrosswalkSignalGreen"]
			else:
				score -= n*user["hitOutsideCrosswalk"]

		elif "OtherCar" in c["geomName"]:
			n1, n2 = calcPercentCar(c["mainCarVel"], c["geomVel"], c["angle"], mc[0])
			score -= (n1*mainCarPassengers*mc[0] + n2*user["otherCarPassengers"]*5 + user["mainCarMaterial"])
		elif "Animal" in c["geomName"]:
			score -= user["animal"]
		elif "Pole" in c["geomName"]:
			n = calcPercentTreePole(r["mainCarVel"], c["angle"])
			score -= (n*mainCarPassengers +user["mainCarMaterial"])
		elif ("Base" in c["geomName"] or "Road" in c["geomName"]):
			score -= (calcPercentRollver()*mainCarPassengers*mc[0] + user["mainCarMaterial"])

	distance, age, gender, velocity = minDist
	if distance < MINDISTMC2P: #discount half of the value of a hit.
		if age == 0:
			if gender == 0:
				collisionValue =user["MaleKid"]
			else:
				collisionValue =user["FemaleKid"]
		elif age == 1:
			if gender == 0:
				collisionValue =user["MaleAdult"]
			else:
				collisionValue =user["FemaleAdult"]
		else:
			if gender == 0:
				collisionValue =user["MaleElderly"]
			else:
				collisionValue =user["FemaleElderly"]
		score -= calcPercentPerson(age, velocity)*collisionValue/2

	if out > MAXOUTDIST: # discount half of the value of a tree/pole collision
		score -= calcPercentTreePole(0, pi/2)*mainCarPassengers/2

	return score

def callGA(simName, island, islandsDone, results, optimumFound):
	fs = FindSolution(Solution, MAXGENERATIONS, POPULATIONSIZE, simName, island)
	fs.run()
	result = {'parameters': fs.getBest().parameters, 'score': fs.getBest().score}
	results.append(result)
	islandsDone.value += 1
	if fs.getBest().score == INICIALSCORE or islandsDone.value == MAXISLANDS:
		optimumFound.set()

def createProcesses(simName):
	gas = []
	with Manager() as manager:
		islandsDone = manager.Value('i', 0)
		optimumFound = manager.Event()
		results = manager.list()
		for i in range(MAXISLANDS):
			p = Process(target=callGA, args = (simName, i, islandsDone, results, optimumFound, ))
			gas.append(p)
			p.start()
		while optimumFound.wait():
			optimumFound.clear()
			print results, islandsDone
			for p in gas:
				p.terminate()
				p.join()
			return max(results, key=lambda s: s['score'])['parameters']

user = {"hitCrosswalkSignalGreen"	:		10000,      \
		"hitCrosswalkSignalRed"		:		5000,	    \
		"hitOutsideCrosswalk"		:		1000,		\
		"MaleKid" 	 				:		10000000,   \
		"MaleAdult"					:		10000000,   \
		"MaleElderly"				:		10000000,   \
		"FemaleKid"					:		10000000,   \
		"FemaleAdult"   			:		10000000,   \
		"FemaleElderly"				:		10000000,   \
		"mainCarSinglePassenger"	:		100000000,  \
		"mainCarDoublePassenger"	:		1000000000,  \
		"mainCarMaterial"			:		10000,      \
		"otherCarPassengers"		:		10000000,   \
		"otherCarMaterial"			:		10000,	    \
		"animal"					:		10000,      \
		}
userPercent = [0.2, 0.0, 0.2, 0.0, 0.2, 0.0, 0.2, 0.0, 0.2, 0.0, 0.2, 0.0, 0.0, 0.0]

if __name__ == '__main__':
	info = sys.argv
	if len(info) == 3:
		filename = "Solutions/" + info[1]
		qnt = int(info[2])
	else:
		print "Informe a name for the file and the quantity of situations to be trained"
		sys.exit()


	try:
		print "Trying to load situations..."
		with open(filename, 'rb') as inputFile:
			solutions = pickle.load(inputFile)
	except:
		print "The file doesn't exist or is broken. Creating a new file and loading situations..."
		solutions = {}
	if not solutions:
		simData = getSituations(qnt, userPercent)
		for sData in simData:
			simName = createName()
			solutions[simName] = {'simData' : sData, 'solution' : None}
		try:
			with open(filename, 'wb') as out:
				pickle.dump(solutions, out)
		except:
			print "Sorry, unable to save file. Try again."
	print "... done"
	print "Starting GA..."
	for key, value in solutions.iteritems():
		if value['solution'] == None:
			try:
				simulationData = value['simData']
				simName = key
				solutions[key]['solution'] = createProcesses(simName)
			except:
				solutions[key]['solution'] = None
		try:
			with open(filename, 'wb') as out:
				pickle.dump(solutions, out)
		except:
			pass
	print "... done" 


"""
optimumFound = False
islandsDone = 0
RESULTS = []
def isOptimum():
	return optimumFound
class callGA(Thread):
	def __init__(self, simName, island):
		#super(callGA, self).__init__()
		Thread.__init__(self)
		self.simName = simName
		self.island = island

	def run(self):
		global optimumFound, islandsDone
		self.fs = FindSolution(Solution, MAXGENERATIONS, self.simName, self.island)
		self.fs.run()
		if self.fs.getBest().score == INICIALSCORE:
			optimumFound = True
			RESULTS.append([self.fs.getBest().parameters, self.fs.getBest().score])
		else:
			RESULTS.append([self.fs.getBest().parameters, self.fs.getBest().score])
			islandsDone += 1

	def stop(self):
		#self.fs.stop()
		print "SSSSSSSSSSSSSSSSSSSSSSSSSSSS"


def createThreads(simName):
	global optimumFound
	gas = []
	for i in range(MAXISLANDS):
		ga = callGA(simName, i)
		gas.append(ga)
		ga.start()
		#ga.join()
		stop = False
	while not stop:
		if (islandsDone == MAXISLANDS or isOptimum()):
			stop = True
	print RESULTS
	for g in gas:

		g.stop()
		#g.terminate()
	return"""

