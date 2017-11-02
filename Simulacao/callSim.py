from simulation import Sim
import json

FILEREAD  = 'jsonParamaters.txt'
FILEWRITE = 'fitness.txt'


with open(FILEREAD) as data:
    jsonParamaters = json.load(data)

dictParameters = json.JSONDecoder().decode(jsonParamaters)

mainCarInfo = dictParameters['mainCarInfo']
roadInfo = dictParameters['roadInfo']
peopleInfo = dictParameters['peopleInfo']
parameters = dictParameters['parameters']
otherCarsInfo = dictParameters['otherCarsInfo']
treepoleInfo = dictParameters['treepoleInfo']
name = dictParameters['name']
test = dictParameters['test']

sim = Sim(mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo, name, test)
sim.start()

fitness = sim.getFitness()

jsonFitness = json.JSONEncoder().encode(fitness)
with open(FILEWRITE, 'w') as outfile:
	json.dump(jsonFitness, outfile)
sim.close()
