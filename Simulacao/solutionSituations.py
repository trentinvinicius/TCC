from genetic import Individual, GeneticAlgorithm
from addNoise import addNoise
import json
import string
from random import randint
import pickle 
from constants import *
import os
from fixedSituations import getSituations

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
						'breakForceFront'	: (0, 1000, 1), \
						'breakForceBack'	: (0, 1000, 1), \
						'amplitude'			: (0, 60, 1), \
						'frequency'			: (0, 100, 1), \
						'phase'				: (0, 1, 1) \
		}
		self.bits_per_gene = 12
		self.length = 5 * self.bits_per_gene
		self.optimization = 11
		Individual.__init__(self, chromosome)

	def evaluate(self, n):
		global simulationData, simName
		#decote bits
		breakForce = [self.decode(0, self.genes['breakForceFront'][0], self.genes['breakForceFront'][1], self.genes['breakForceFront'][2]), \
					  self.decode(1, self.genes['breakForceBack'][0], self.genes['breakForceBack'][1], self.genes['breakForceBack'][2])]
		amplitude  =  self.decode(2, self.genes['amplitude'][0], self.genes['amplitude'][1], self.genes['amplitude'][2])
		frequency  =  self.decode(3, self.genes['frequency'][0], self.genes['frequency'][1], self.genes['frequency'][2])
		phase 	   =  self.decode(4, self.genes['phase'][0], self.genes['phase'][1], self.genes['phase'][2])	
		self.parameters = [breakForce, float(amplitude)/2, float(frequency)/100, phase]
		#add a little noise to the data
		mc, r, oc, p, a, tp = addNoise(simulationData)

		msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
		   	   "animalInfo": a, "parameters": self.parameters, "name": simName, "test" : False, "visualization" : False}

		jsonSim = json.JSONEncoder().encode(msg)

		with open(FILEWRITE, 'w') as outfile:
			json.dump(jsonSim, outfile)
		
		os.system('python callSim.py')
		with open(FILEREAD) as data:
			jsonResult = json.load(data)

		result = json.JSONDecoder().decode(jsonResult)
		print n, ": ", result

		#score = userEvaluate(result)

		self.score = n

class FindSolution(GeneticAlgorithm):
	def __init__(self, kind, maxgenerations, simName):
		self.filename = 'Genetic/' + simName
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
		"se dois ou mais forem bons, escolher o com menor frequencia"
		self.population.sort(key = lambda x: x.score, reverse = True)
		return self.population[:num]	

#local functions
def createName():
	name = ''.join([char_set[randint(0, len(char_set) - 1)] for i in range(5)])
	while name in names:
		name = ''.join([char_set[randint(0, len(char_set) - 1)] for i in range(5)])
	names.append(name)
	with open('Solutions/names.txt', 'w') as outfile:
		json.dump(names, outfile)
	return name

def userEvaluate():
	return 1


if __name__ == '__main__':

	info = sys.argv
	if len(info) == 3:
		filename = info[1]
		qnt = info[2]
	else:
		print "Informe a name for the file and the quantity of situations to be trained"
		sys.exit()


	'''
	entra com um nome de usuario por exemplo
	pega 1000 situations da fixed
	mais umas da outra
	faz tudo
	cria uma funcao fora para o evaluate e da um return com o score
	criar dict de dict
	{simName = {'simulationData' = sD, 'solution' = solution}}
	quando pegar nova simulacao ja salvar dict com 'solution' = notFound sei la
	'''

	'''

	mainCarInfo = (3, 30, 0)
	roadInfo = (4, 1, 2, 10, 0)
	peopleInfo = [((10, 0, 2), 2, 97, 0, 0, 0)]	
	treepoleInfo = None# [(10, 0, 1, 0), (15, 0, 0, 1), (12, 1, 1, 2), (18, 1, 0, 3), (21, 0, 1, 4), (24, 0, 1, 5), (27, 0, 0, 6), (30, 0, 0, 7)]
	otherCarsInfo = [[[70, 0, -3.0], 1, 10.125, 0],[[50, 0, -3.0], 1, 10.125, 0]]
	animalInfo = None
	simData = [[mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, animalInfo, treepoleInfo]]


	'''
	simData = getSituations(1000)
	solutions = {}
	for simulationData in simData:
		simName = createName()
		solucoes[simName] = {'simData' : simulationData, 'solution' = None}
		fs = FindSolution(Solution, 200, simName)
		fs.run()
		solucoes[simName]['solution'] = fs.getBest().parameters

