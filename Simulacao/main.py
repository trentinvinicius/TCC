from simulation import Sim
from math import pi 
import os
import json
import sys
from constants import *


def createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, parameters, name):
	msg = {"mainCarInfo": mainCarInfo, "roadInfo": roadInfo, "peopleInfo": peopleInfo, "otherCarsInfo": otherCarsInfo, "treepoleInfo": treepoleInfo, \
		   "parameters": parameters, "name": name, "test" : False}
	return json.JSONEncoder().encode(msg)
	
mainCarInfo = (3, 1, 0)
roadInfo = (4, 1, 2)
peopleInfo = [((-0, 0, 17), (0, 0, 0))]
treepoleInfo = [(10, 0, 1), (15, 0, 0), (12, 1, 1), (18, 1, 0), (21, 0, 1), (24, 0, 1), (27, 0, 0), (30, 0, 0)]
otherCarsInfo = [((7, 0, -3), -1, 10), ((17, 0, -3), -1, 10)]
parameters = [-0, 1, 1, pi/2]

if __name__ == '__main__':
	infos = sys.argv
	if (len(infos) == 2):
		inputFile = infos[1]
	else:
		print "Informe the simulation data file"
		sys.exit()
	with open(inputFile) as data:
		jsonSimInfos = json.load(data)

	simInfos = json.JSONDecoder().decode(jsonSimInfos)

	for i in range(len(simInfos)):

		#mainCarInfo, roadInfo, otherCarsInfo, peopleInfo, treepoleInfo = simInfos[i]
		jsonParameters = createJSON(mainCarInfo, roadInfo, peopleInfo, treepoleInfo, otherCarsInfo, parameters, "banana")
		
		with open(FILEWRITE, 'w') as outfile:
			json.dump(jsonParameters, outfile)
		
		os.system('python callSim.py')
		
		with open(FILEREAD) as data:
			jsonFitness = json.load(data)

		fitness = json.JSONDecoder().decode(jsonFitness)
		print i, fitness




