from random import *
from constants import *
import sys
import json
import os
import numpy as np
from math import exp, pi, cos, sin
import string
from PIL import Image
from genetic import Individual, GeneticAlgorithm
from math import cos, sin, pi
import pylab as plt
import pickle 

# getting the simulations names
try:
	with open('Situations/names.txt') as data:
		names = json.load(data)
except:
	names = []

# set of possivels values for the name of the simulation
char_set = string.ascii_uppercase + string.digits



visualization = False


class Situation(Individual):
	def __init__(self, chromosome = None):
		self.genes = { \
						'mainCar'   : { 'passangerNum' 		: (1, MAXPASSANGERS, 1), \
									    'velocity' 		    : (MINVELOCITY, MAXVELOCITY, 0)}, \
						'road'    	: { 'direction'    		: (0, 1, 1), \
									    'numLanes'	 		: (1, 8, 1), \
									    'mainCarLane'  		: (1, '', 1), \
									    'crosswalk'	 		: (0, 1, 1), \
									    'crossPos'	 		: (MINCROSSPOS, MAXCROSSPOS, 0), \
									    'statusSemaphore'	: (0, 1, 1)}, \
						'otherCars' : { 'qnt'				: (0, MAXNUMOTHERCARS, 1), \
										'direction'			: (0, '', 1), \
										'xPosition'			: (MINDISTOTHERCAR, MAXDISTOTHERCAR, 0), \
										'lane'				: ('', '', 1), \
										'velocity'			: (MINVELOCITY, MAXVELOCITY, 0)}, \
						'people'	: { 'qnt'				: (1, MAXNUMPEOPLE, 1), \
										'xPos'				: (MINXDISTPERSON, MAXXDISTPERSON, 0), \
										'zPos'				: (MINZDISTPERSON, MAXZDISTPERSON, 0), \
										'velocity'			: (MINVELPERSON, MAXVELPERSON, 0), \
										'orientation'		: (0, 360, 0), \
										'gender'			: (0, 1, 1), \
										'age'				: (0, 2, 1) }, \
						'animal' 	: { 'qnt'				: (0, MAXNUMANIMAL, 1), \
										'xPos'				: (MINXDISTANIMAL, MAXXDISTANIMAL, 0), \
										'zPos'				: (MINZDISTANIMAL, MAXZDISTANIMAL, 0), \
										'velocity'			: (MINVELANIMAL, MAXVELANIMAL, 0), \
										'orientation'		: (0, 360, 0)}, \
						'treepole'  : { 'qnt'				: (0, MAXNUMTREEPOLE, 1), \
										'xPos'				: (MINDISTTREEPOLE, MAXDISTTREEPOLE, 0), \
										'side'				: (0, 1, 1), \
										'type'				: (0, 1, 1)} \
		} 
		self.bits_per_gene = 10
		self.length = TOTALNUMGENESSIM
		self.optimization = 11
		Individual.__init__(self, chromosome)
                                                                                                         
	def mainCar(self): # passanger number, velocity
	   genes = self.genes['mainCar']
	   passangerNum = self.decode(0, genes['passangerNum'][0], genes['passangerNum'][1], genes['passangerNum'][2])
	   velocity = self.decode(1, genes['velocity'][0], genes['velocity'][1], genes['velocity'][2])
	   steerAngle = 0.0
	   return [passangerNum, velocity, steerAngle]

	def road(self): # numLanes, direction, mainCarLane, crosswalk, crossPos, statusSemaphore
		genes = self.genes['road']
		direction = self.decode(2, genes['direction'][0], genes['direction'][1], genes['direction'][2])
		numLanes = self.decode(3, genes['numLanes'][0], genes['numLanes'][1], genes['numLanes'][2])
		if (numLanes > 4):
			direction = 1
		if (direction):
			if (numLanes % 2 == 1):
				numLanes += 1
			aux = numLanes / 2
		else:
			aux = numLanes
		mainCarLane =  self.decode(4, genes['mainCarLane'][0], aux, genes['mainCarLane'][2])
		crosswalk = self.decode(5, genes['crosswalk'][0], genes['crosswalk'][1], genes['crosswalk'][2])
		if crosswalk:
			crossPos = self.decode(6, genes['crossPos'][0], genes['crossPos'][1], genes['crossPos'][2])
			statusSemaphore = self.decode(7, genes['statusSemaphore'][0], genes['statusSemaphore'][1], genes['statusSemaphore'][2])
		else:
			crossPos = 0
			statusSemaphore = 0
		return (numLanes, direction, mainCarLane, crossPos, statusSemaphore)

	def otherCars(self, numLanes, roadDirection, mainCarLane): # pos, direction, velocity
		i = 8
		genes = self.genes['otherCars']
		otherCarsInfo = []
		for j in range(self.decode(i, genes['qnt'][0], genes['qnt'][1], genes['qnt'][2])):
			direction = self.decode(i + j*4 + 1, genes['direction'][0], roadDirection, genes['direction'][2])
			x = self.decode(i + j*4 + 2, genes['xPosition'][0], genes['xPosition'][1], genes['xPosition'][2])
			if direction:
				aux1 = numLanes/2 + 1
				aux2 = numLanes
				direction = - 1
			else:
				aux1 = 1
				aux2 = numLanes/2
				direction = 1
			lane = self.decode(i + j*4 + 3, aux1, aux2, genes['lane'][2])
			velocity = self.decode(i + j*4 + 4, genes['velocity'][0], genes['velocity'][1], genes['velocity'][2])	
			posZ = (mainCarLane - lane)*ROADSIZE
			otherCarsInfo.append([(x, 0, posZ), direction, velocity, j])
		return otherCarsInfo

	def people(self): #pos, velocity, orientation
		i = 8 + MAXNUMOTHERCARS*4 + 1
		genes = self.genes['people']
		peopleInfo = []
		for j in range(self.decode(i, genes['qnt'][0], genes['qnt'][1], genes['qnt'][2])):
			x 		= 		self.decode(i + j*6 + 1, genes['xPos'][0], genes['xPos'][1], genes['xPos'][2])
			z 		= 		self.decode(i + j*6 + 2, genes['zPos'][0], genes['zPos'][1], genes['zPos'][2])
			v 		= 		self.decode(i + j*6 + 3, genes['velocity'][0], genes['velocity'][1], genes['velocity'][2])
			o 		= 		self.decode(i + j*6 + 4, genes['orientation'][0], genes['orientation'][1], genes['orientation'][2])
			gender  = 		self.decode(i + j*6 + 5, genes['gender'][0], genes['gender'][1], genes['gender'][2])
			age 	= 		self.decode(i + j*6 + 6, genes['age'][0], genes['age'][1], genes['age'][2])
			peopleInfo.append([(x, 0, z), v, o, gender, age, j])
		return peopleInfo

	def animal(self): #pos, velocity, orientation
		i = 8 + MAXNUMOTHERCARS*4 + MAXNUMPEOPLE*4 + 1
		genes = self.genes['animal']
		animalInfo = []
		for j in range(self.decode(i, genes['qnt'][0], genes['qnt'][1], genes['qnt'][2])):
			x = self.decode(i + j*4 + 1, genes['xPos'][0], genes['xPos'][1], genes['xPos'][2])
			z = self.decode(i + j*4 + 2, genes['zPos'][0], genes['zPos'][1], genes['zPos'][2])
			v = self.decode(i + j*4 + 3, genes['velocity'][0], genes['velocity'][1], genes['velocity'][2])
			o = self.decode(i + j*4 + 4, genes['orientation'][0], genes['orientation'][1], genes['orientation'][2])
			animalInfo.append([(x, 0, z), v, o, j])
		return animalInfo

	def treepole(self): # pos, side, type
		i = 8 + MAXNUMOTHERCARS*4 + MAXNUMPEOPLE*4 + MAXNUMANIMAL*4 + 1
		genes = self.genes['treepole']
		treepoleInfo = []
		for j in range(self.decode(i, genes['qnt'][0], genes['qnt'][1], genes['qnt'][2])):
			x = self.decode(i + j*3 + 1, genes['xPos'][0], genes['xPos'][1], genes['xPos'][2])
			side = self.decode(i + j*3 + 2, genes['side'][0], genes['side'][1], genes['side'][2])
			tipo = self.decode(i + j*3 + 3, genes['type'][0], genes['type'][1], genes['type'][2])
			treepoleInfo.append((x, side, tipo, j))
		return treepoleInfo

	def createName(self):
		name = ''.join([char_set[randint(0, len(char_set) - 1)] for i in range(5)])
		while name in names:
			name = ''.join([char_set[randint(0, len(char_set) - 1)] for i in range(5)])
		names.append(name)
		return name

	def evaluate(self, n, _, generation):
		global visualization
		self.mainCarData = self.mainCar()
		self.roadData = self.road()
		self.otherCarsData = self.otherCars(self.roadData[0], self.roadData[1], self.roadData[2])
		self.peopleData = self.people()
		self.animalData = self.animal()
		self.treepoleData = self.treepole()
		#create vector with all data for the images
		self.allData = [self.mainCarData, self.roadData, self.otherCarsData, self.peopleData, self.animalData, self.treepoleData]
		#create images before updating the distances
		#self.createImages()
		
		self.msg = {"mainCarInfo": self.mainCarData, "roadInfo": self.roadData, "peopleInfo": self.peopleData, "otherCarsInfo": self.otherCarsData, "treepoleInfo": self.treepoleData, \
		   	   "animalInfo": self.animalData, "parameters": [0, 0, 0, 0, 0], "name": "Teste", "test" : True, "visualization" : visualization}

		jsonSim = json.JSONEncoder().encode(self.msg)

		with open(FILEWRITE, 'w') as outfile:
			json.dump(jsonSim, outfile)
		
		os.system('python callSim.py')
		with open(FILEREAD) as data:
			jsonResult = json.load(data)

		result = json.JSONDecoder().decode(jsonResult)
		if result == True:
			self.score = -100000
		else:
			result = np.array(result)
			score = sum(np.multiply(result[:13], goal)) 
			if goal[0] != 0 and goal[1] != 0:
				score += 100000 - 100*(result[13])
			if (goal[0] > goal[1]):
				score += 100000 - 100*(result[14])
			self.score = score
		print "{} SCORE: {} and RESULT {}".format(n, self.score, result)
		print goal

class CreateSituations(GeneticAlgorithm):
	def __init__(self, filename, kind, maxgenerations):
		self.filename = filename
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
				maxgenerations=maxgenerations, \
				generation=generation)

	def report(self):
		# Report results and save
		print '='*70					
		print "generation: ", self.generation
		print "best:       ", self.best		
		print "="*70
									
		data = { 						
				'population':self.population, \
				'generation':self.generation, \
		}
		pickle.dump(data, open(self.filename,'wb'))

	def getBest(self, num):
		self.population.sort(key = lambda x: x.score, reverse = True)
		return self.population[:num]

	

def call(goalInfo, name, viz, size):
	global goal
	global visualization
	visualization = viz
	
	goal = np.zeros(13)
	try:
		if (len(goalInfo) != 4):
			raise
		#person
		if (int(goalInfo[0]) > 0):
			if (int(goalInfo[0]) == 1):
				goal[0] = 1000000
				goal[1] = 500000
			else:
				goal[0] = 500000
				goal[1] = 1000000
			if int(goalInfo[1]) == 1:
				goal[2] = 1000000
			goal[3 + int(goalInfo[2])] = 1000000
		print goal
		#animal
		goal[9] = int(goalInfo[3])*1000000
		'''goal = [10**int(g) for g in list(goal)]
		if len(goal) != 6:
			raise'''
	except:
		#print "Goals example: 654321 people in the crosswalk, people not in the crosswalk, animal, other car, pole, road"
		print "Goals example: WXYZ \n \
				W = 0 : no person, 1 : people in the crosswalk, 2 : people not in the crosswalk \n \
				X = statusSemaphore \n \
				Y = 0 : MaleKid, 1 : MaleMiddle, 2: MaleOld, 3: FemaleKid, 4 : FemaleMiddle, 5 : FemaleOld \n \
				Z = animal"
		sys.exit()
	outputFile = "Situations/" + name
	geneticFile = "Genetic/" + name

	cs = CreateSituations(geneticFile, Situation, maxgenerations = size)
	cs.run()

	
	best = cs.getBest(30)
	'''msg e allData'''

	with open(outputFile, 'w') as out:
		pickle.dump(best, out)
	'''

	#criar dicionario com os melhores com nome, imagens e simulacao salvar com o nome do arquivo
	#colocar pessoa com cachorro, 4 posicoes na frente do carro 0000 lateral 2? com arvore
	jsonSimInfos = json.JSONEncoder().encode(simInfos)
	with open(outputFile, 'w') as out:
		json.dump(jsonSimInfos, out)

	with open("Situations/names.txt", 'w') as out:
		json.dump(names, out)
	'''
