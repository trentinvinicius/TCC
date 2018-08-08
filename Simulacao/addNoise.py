from constants import *
from random import uniform


def addNoise(simulationData, dataType = None):
	# general
	if (dataType == None):
		try:
			mc, r, oc, people, animal, tp, river = simulationData
			aux = True
		except:
			mc, r, oc, people, animal, tp = simulationData
		newPeople = []
		for p in people:
			pos, v, o, g, a, n = p
			x, _, z = pos
			x += uniform(-POSNOISE, POSNOISE)
			z += uniform(-POSNOISE, POSNOISE)
			v += abs(uniform(-VELOCITYNOISE, VELOCITYNOISE))
			o += uniform(-ORIENTATIONNOISE, ORIENTATIONNOISE)
			newPeople.append([(x, 0, z), v, o, g, a, n])
		newAnimal = []
		if animal != None:
			for a in animal:
				pos, v, o, n = a
				x, _, z = pos
				x += uniform(-POSNOISE, POSNOISE)
				z += uniform(-POSNOISE, POSNOISE)
				v += abs(uniform(-VELOCITYNOISE, VELOCITYNOISE))
				o += uniform(-ORIENTATIONNOISE, ORIENTATIONNOISE)
				newAnimal.append([(x, 0, z), v, o, n])
		if aux:
			return [mc, r, oc, newPeople, newAnimal, tp, river]
		else:
			return [mc, r, oc, newPeople, newAnimal, tp]
	
	# people
	elif (dataType == "people"):
		newPeople = []
		for p in simulationData:
			pos, v, o, g, a, n = p
			x, _, z = pos
			x += uniform(-POSNOISE, POSNOISE)
			z += uniform(-POSNOISE, POSNOISE)
			v += abs(uniform(-VELOCITYNOISE, VELOCITYNOISE))
			o += uniform(-ORIENTATIONNOISE, ORIENTATIONNOISE)
			newPeople.append([(x, 0, z), v, o, g, a, n])
		return newPeople
	#animal
	elif (dataType == "animal"):
		newAnimal = []
		if simulationData != None:
			for a in simulationData:
				pos, v, o, n = a
				x, _, z = pos
				x += uniform(-POSNOISE, POSNOISE)
				z += uniform(-POSNOISE, POSNOISE)
				v += abs(uniform(-VELOCITYNOISE, VELOCITYNOISE))
				o += uniform(-ORIENTATIONNOISE, ORIENTATIONNOISE)
				newAnimal.append([(x, 0, z), v, o, n])
		return newAnimal


