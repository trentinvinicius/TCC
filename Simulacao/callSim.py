from simulation import Sim
import json
import sys

info = sys.argv
if len(info) == 2:
	FILEREAD = 'jsonParamaters' + info[1] + '.txt'
	FILEWRITE = 'fitness' + info[1] + '.txt'
else:
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
animalInfo = dictParameters['animalInfo']
name = dictParameters['name']
test = dictParameters['test']
visualization = dictParameters['visualization']
try:
	color = dictParameters['color']
except:
	color = 0
try:
	riverInfo = dictParameters['riverInfo']
except:
	riverInfo = [False, 0]
try:
	folderToSave = dictParameters['folderToSave']
except:
	folderToSave = None
try:
	drawTrajectory = dictParameters['drawTrajectory']
except:
	drawTrajectory = False
	
sim = Sim(mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo, animalInfo, riverInfo, name, test, visualization, color, folderToSave, drawTrajectory)

sim.simulate()

result = sim.getResult()

jsonResult = json.JSONEncoder().encode(result)
with open(FILEWRITE, 'w') as outfile:
	json.dump(jsonResult, outfile)
sim.close()
