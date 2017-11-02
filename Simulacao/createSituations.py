from random import *
from constants import *
import sys
import json
import os

'''
agrupar situacoes em categorias
'''

with open('velocTimeDist.txt') as data:
	velDistTime = json.load(data)

tempos = []
distancia = []
vel = []

for vdt in velDistTime:
	vel.append(vdt[0])
	tempos.append(vdt[1][0])
	distancia.append(vdt[1][1])


carTempo = []


def mainCar(): # passanger number, velocity
   passangerNum = randint(MINPASSANGERNUM, MAXPASSENGERNUM)
   velocity = uniform(MINVELOCITY, MAXVELOCITY)
   velId = [i for i, x in enumerate(vel) if x >= velocity][0]
   dist = (distancia[velId] - distancia[velId - 1])*(velocity - vel[velId]) + distancia[velId]
   tempo = (tempos[velId] - tempos[velId - 1])*(velocity - vel[velId]) + tempos[velId]
   steerAngle = 0.0
   carTempo.append(tempo)
   return [passangerNum, velocity, steerAngle, dist, tempo]

def road(): # numLanes, direction, mainCarLane
	direction = randint(0, 1)
	numLanes = randint(1, MAXLANENUM)
	if numLanes > 4:
		direction = 1
	if direction == 1:
		while(numLanes % 2 == 1):
			numLanes = randint(1, MAXLANENUM)
		aux = numLanes/2
	else:
		aux = numLanes
	mainCarLane = randint(1, aux)
	return (numLanes, direction, mainCarLane)

def otherCars(numLanes, roadDirection, mainCarLane): # pos, direction, velocity
	n = randint(0, MAXNUMOTHERCARS)
	if (n == 0):
		otherCarsInfo = None
	else:
		otherCarsInfo = []
		for i in range(n):
			x = uniform(MINDISTOTHERCAR, MAXDISTOTHERCAR)
			if roadDirection:
				direction = randint(0, 1)
				z = randint(1, numLanes/2) + (1 - direction)*numLanes/2
				if (direction == 0):
					direction = -1
					aux = 1
			else:
				direction = 1
				aux = -1
				z = randint(1, numLanes)
			velocity = uniform(MINVELOCITY, MAXVELOCITY)
			velId = [i for i, x in enumerate(vel) if x >= velocity][0]
	   		dist = (distancia[velId] - distancia[velId - 1])*(velocity - vel[velId]) + distancia[velId]
	   		tempo = (tempos[velId] - tempos[velId - 1])*(velocity - vel[velId]) + tempos[velId]
	   		carTempo.append(tempo)
	   		#x +=  aux*dist
			otherCarsInfo.append([(x, 0, z), direction, velocity, dist, tempo])
	return otherCarsInfo

def people(): #pos, velocity
	n = randint(1, MAXNUMPEOPLE)
	peopleInfo = []
	for i in range(n):
		x  = uniform(MINXDISTPERSON, MAXXDISTPERSON)
		z  = uniform(MINZDISTPERSON, MAXZDISTPERSON)
		vx = uniform(MINXVELPERSON,  MAXXVELPERSON)
		vz= uniform(MINZVELPERSON,  MAXZVELPERSON)
		peopleInfo.append(((x, 0, z), (vx, 0, vz)))
	return peopleInfo

def treepole(): # pos, side, type
	n = randint(0, MAXNUMTREEPOLE)
	if (n == 0):
		treepoleInfo = None
	else:
		treepoleInfo = []
		for i in range(n):
			x = uniform(MINDISTTREEPOLE, MAXDISTTREEPOLE)
			side = randint(0, 1)
			tipo = randint(0, 1)
			treepoleInfo.append((x, side, tipo))
	return treepoleInfo

if __name__ == '__main__':
	infos = sys.argv
	if len(infos) == 3:
		num = int(infos[1])
		outputFile = infos[2]
	else:
		print "Informe the number of simulations and the output file"
		sys.exit()
	n = 0
	simInfos = []
	while (n < num):
		sim = []
		mainCarData = mainCar()
		roadData = road()
		otherCarsData = otherCars(roadData[0], roadData[1], roadData[2])
		peopleData = people()
		treepoleData = treepole()
		#update distances according to the maximum time	
		maxTempo = max(carTempo)
		mainCarData[3] += mainCarData[1]*(maxTempo - mainCarData[4])
		if otherCarsData != None:
			for ocd in otherCarsData:
				ocd[3] += ocd[2]*(maxTempo - ocd[4])
		sim.append(mainCarData)
		sim.append(roadData)
		sim.append(otherCarsData)
		sim.append(peopleData)
		sim.append(treepoleData)

		msg = {"mainCarInfo": mainCarData, "roadInfo": roadData, "peopleInfo": peopleData, "otherCarsInfo": otherCarsData, "treepoleInfo": treepoleData, \
		   	   "parameters": [0, 0, 0, 0], "name": "Teste", "test" : True}

		jsonSim = json.JSONEncoder().encode(msg)
	

		with open(FILEWRITE, 'w') as outfile:
			json.dump(jsonSim, outfile)
		
		os.system('python callSim.py')
		
		with open(FILEREAD) as data:
			jsonFitness = json.load(data)

		fitness = json.JSONDecoder().decode(jsonFitness)
		print fitness
		simInfos.append(sim)
		n += 1
		print sim

	jsonSimInfos = json.JSONEncoder().encode(simInfos)
	with open(outputFile, 'w') as out:
		json.dump(jsonSimInfos, out)

