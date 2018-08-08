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
from multiprocessing import Process, Manager, cpu_count
import numpy as np
from time import sleep

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
		self.length = 5 * self.bits_per_gene
		self.optimization = 11
		Individual.__init__(self, chromosome)
		#decote bits		
		breakForce =  self.decode(0, self.genes['brakeForce'][0], self.genes['brakeForce'][1], self.genes['brakeForce'][2])
		amplitude  =  self.decode(1, self.genes['amplitude'][0], self.genes['amplitude'][1], self.genes['amplitude'][2])
		frequency  =  self.decode(2, self.genes['frequency'][0], self.genes['frequency'][1], self.genes['frequency'][2])
		phase 	   =  self.decode(3, self.genes['phase'][0], self.genes['phase'][1], self.genes['phase'][2])
		delay 	   =  self.decode(4, self.genes['delay'][0], self.genes['delay'][1], self.genes['delay'][2])	
		self.parameters = [breakForce, float(amplitude)/2, float(frequency)/100, phase, float(delay)/5]

	def evaluate(self, n, island, generation, possible_optimum = False):
		try:
			global simulationData, simName
			#files to send and get data to/from the simulation
			FILEWRITE = 'jsonParamaters' + str(island) + '.txt'
			FILEREAD = 'fitness' + str(island) + '.txt'
			accumuated_score = 0

			for i in range(NUMSIMPERINDIVIDUAL if not possible_optimum else 10):
				if i == 0:
					try:
						mc, r, oc, p, a, tp, river = simulationData
					except:
						mc, r, oc, p, a, tp = simulationData
						river = [False, 0]
				else:
					try:
						mc, r, oc, p, a, tp, river = addNoise(simulationData)
					except:
						mc, r, oc, p, a, tp = addNoise(simulationData)
						river = [False, 0]

				msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
				   	   "animalInfo": a, "riverInfo": river, "parameters": self.parameters, "name": simName, "test" : False, "visualization" : False}

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
			self.score = accumuated_score/(NUMSIMPERINDIVIDUAL if not possible_optimum else 10.0)
		except Exception as e:
			exc_type, exc_obj, exc_tb = sys.exc_info()
			fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
			print exc_type, fname, exc_tb.tb_lineno
			print "Error aqui segundo erro linha 85", e, island
			self.score = -10.0*INICIALSCORE

		#print "Generation {}, island {}, individual {}, score {}".format(generation, island, n, self.score)

class FindSolution(GeneticAlgorithm):
	def __init__(self, kind, maxgenerations, size, simName, island, inicialPopulation = None):
		self.filename = 'Genetic/Solutions/' + simName + str(island)
		try:						
			data = pickle.load(open(self.filename,'rb'))	
		except:						
			data = {}
		if 'population' in data:		
			population = data['population']
		else:							
			population = inicialPopulation or None				
		if 'generation' in data:			
			generation = data['generation']	
			#APENAS PARA CORRIGIR ERRO CASO EXISTA
			#if generation > 30:
			#	generation = 30
			#FIM	
		else:						
			generation = 0

		self.lastScores = np.zeros(CONVERGELENGTH)
		GeneticAlgorithm.__init__(self, kind, population=population, \
				maxgenerations=maxgenerations, size = size, \
				generation=generation, optimum = INICIALSCORE, island = island)

	def report(self):
		# Report results and save
		print '='*70					
		print "generation: ", self.generation, "island: ", self.island, "simName: ", simName
		print "best:       ", self.best		
		print "="*70
									
		data = { 						
				'population':self.population, \
				'generation':self.generation, \
		}
		pickle.dump(data, open(self.filename,'wb'))
		self.lastScores[self.generation % CONVERGELENGTH] = self.best.score
		#print self.lastScores
		if np.std(self.lastScores) < MINSTD:
			self.hasConverged = True

	def getBest(self):
		self.population.sort(key = lambda x: x.score, reverse = True)
		return self.population[0:50]

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
			mainCarVel  *= 3.6
			otherCarVel *= 3.6
			factor = sqrt(mainCarVel**2 + otherCarVel**2 - 2*mainCarVel*otherCarVel*cos(angle)) / (m1 + m2)
			deltaV1 = m2*factor
			deltaV2 = m1*factor
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
	for ir in inRiver:
		if ir == "MainCar":
			score -= mainCarPassengers
		elif "OtherCar" in ir:
			score -= user["otherCarPassengers"]
		elif "Person" in ir:
			if "Kid" in ir:
				if "Male" in ir:
					score -= user["MaleKid"]
				else:
					score -= user["FemaleKid"]
			elif "Adult" in ir:
				if "Male" in ir:
					score -= user["MaleAdult"]
				else:
					score -= user["FemaleAdult"]
			else:
				if "Male" in ir:
					score -= user["MaleElderly"]
				else:
					score -= user["FemaleElderly"]

	for c in collisions:
		if (road[3] > 0 and (road[3] - 1.5 <= c["pos"] <= road[3] + 1.5)):
			if road[4]: #signal open for cars
				factor = user["hitCrosswalkSignalRed"]
			else:
				factor = user["hitCrosswalkSignalGreen"]
		else:
			factor = user["hitOutsideCrosswalk"]
		if "Person" in c["geomName"]:
			if "Kid" in c["geomName"]:
				if "Male" in c["geomName"]:
					n = calcPercentPerson(0, c["mainCarVel"])
					score -= n*factor*user["MaleKid"]
				else:
					n = calcPercentPerson(0, c["mainCarVel"])
					score -= n*factor*user["FemaleKid"]
			elif "Adult" in c["geomName"]:
				if "Male" in c["geomName"]:
					n = calcPercentPerson(1, c["mainCarVel"])
					score -= n*factor*user["MaleAdult"]
				else:
					n = calcPercentPerson(1, c["mainCarVel"])
					score -= n*factor*user["FemaleAdult"]
			else:
				if "Male" in c["geomName"]:
					n = calcPercentPerson(2, c["mainCarVel"])
					score -= n*factor*user["MaleElderly"]
				else:
					n = calcPercentPerson(2, c["mainCarVel"])
					score -= n*factor*user["FemaleElderly"]

		elif "OtherCar" in c["geomName"]:
			n1, n2 = calcPercentCar(c["mainCarVel"], c["geomVel"], c["angle"], mc[0])
			score -= (n1*mainCarPassengers + n2*user["otherCarPassengers"] + MATERIALCOST)
		elif "Animal" in c["geomName"]:
			score -= factor*user["animal"]
		elif "Pole" in c["geomName"]:
			n = calcPercentTreePole(c["mainCarVel"], c["angle"])
			score -= (n*mainCarPassengers)
		elif ("Base" in c["geomName"] or "Road" in c["geomName"]):
			score -= (calcPercentRollver()*mainCarPassengers)
		elif ("River" in c["geomName"]):
			score -= mainCarPassengers

	if len(minDist) == 4:
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
			elif age == 2:
				if gender == 0:
					collisionValue =user["MaleElderly"]
				else:
					collisionValue =user["FemaleElderly"]
			else:
				collisionVaue = 0
			score -= calcPercentPerson(age, velocity)*user["hitCrosswalkSignalGreen"]*collisionValue*(1 + MINDISTMC2P - distance)/4
	if out > MAXOUTDIST: # discount half of the value of a tree/pole collision
		score -= calcPercentTreePole(0, pi/2)*mainCarPassengers/2
	return score

def callGA(name, simData, userPreferences, island, islandsDone, results, optimumFound, simDict, doneList, statusSituation, numIslands, inicialPopulation = None):
	try:
		global simulationData, user, simName
		simName = name
		simulationData = simData
		user = userPreferences
		fs = FindSolution(Solution, MAXGENERATIONSPYRAMID, POPULATIONSIZE, simName, island, inicialPopulation)
		fs.run()
		results.insert(0, fs.getBest())
		islandsDone.value += 1
		doneList.append([name, island])
		if fs.getBest()[0].score == INICIALSCORE or (islandsDone.value == 1 and numIslands == 1):
			optimumFound.set()
		if islandsDone.value == numIslands:
			statusSituation.set()
		simDict[name]['results'] = results
		simDict[name]['islandsDone'] = islandsDone.value
		simDict[name]['optimumFound'] = optimumFound
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
    		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    		print exc_type, fname, exc_tb.tb_lineno
		print "Error aqui", e, island


