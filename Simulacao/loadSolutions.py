import pickle
import sys
import json
import os

info = sys.argv
FILEWRITE = 'jsonParamaters.txt'

try:
	filename = 'Solutions/' + info[1]
	print "Trying to load situations..."
	with open(filename, 'rb') as inputFile:
		solutions = pickle.load(inputFile)
except:
	sys.exit()

i = 0

for key, value in solutions.iteritems():
	if value['solution'] != None:
		print i
		i += 1
		for j, p in enumerate(value['solution']):
			print j, p.score
		

		simulationData = value['simData']
		parameters = value['solution']
		simName = key
		mc, r, oc, p, a, tp = simulationData
		msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
			   	   "animalInfo": a, "parameters": parameters, "name": simName, "test" : False, "visualization" : True}

		jsonSim = json.JSONEncoder().encode(msg)

		with open(FILEWRITE, 'w') as outfile:
			json.dump(jsonSim, outfile)

		call = 'python callSim.py'
		os.system(call)
		"Para excluir alguma solucao especifica"
		'''
		i += 1
		if i == 40:
			print "AQUI"
			solutions[key]['solution'] = None
			print value['solution']
			with open(filename, 'wb') as out:
				pickle.dump(solutions, out)
		'''