import json
import os
import pickle
import sys
from time import sleep
from addNoise import addNoise
from saveSituationLatexTable import saveSituationLatexTable

def loadFile(mainFileName):
	with open(mainFileName, 'rb') as inputFile:
		mainFile = pickle.load(inputFile)
	return mainFile

def show(s, folderToSave):
	FILEWRITE = 'jsonParamaters.txt'
	FILEREAD = 'fitness.txt'
	print s['simName']
	try:
		mc, r, oc, p, a, tp, river = s['simData']
	except:
		mc, r, oc, p, a, tp = s['simData']
		river = [False, 0]

	#print mc, r
	
	p.append([(18, 0, 2.4), 1, 90, 1, 2, 0])
	p.append([(16, 0, 7), 1, 90, 1, 0, 0])
	a = [[(19, 0, 0), 1, 91, 0]]

	#simData = [mc, r, oc, p, a, tp, river]
	#mc, r, oc, p, a, tp, river = addNoise(simData)
	if folderToSave != None:
		if '1' in folderToSave:
			colorMainCar = 0
		else:
			colorMainCar = 1
	else:
		colorMainCar = 0
	msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
		   "animalInfo": a, "riverInfo": river, "parameters": s['solution'], "name": s['simName'], "test" : False, "visualization" : True, "folderToSave": folderToSave, 'color': colorMainCar}
	saveSituationLatexTable(msg, folderToSave)
	return

	jsonSim = json.JSONEncoder().encode(msg)

	with open(FILEWRITE, 'w') as outfile:
		json.dump(jsonSim, outfile)

	call = 'python callSim.py'
	os.system(call)
	saveSituationLatexTable(msg, folderToSave)

	drawTrajectory = False if folderToSave == None else True

	msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
		   "animalInfo": a, "riverInfo": river, "parameters": s['solution'], "name": s['simName'], "test" : False, "visualization" : True, "folderToSave": folderToSave, 'drawTrajectory': drawTrajectory, 'color': colorMainCar}

	jsonSim = json.JSONEncoder().encode(msg)

	with open(FILEWRITE, 'w') as outfile:
		json.dump(jsonSim, outfile)

	call = 'python callSim.py'
	os.system(call)
	with open(FILEREAD) as data:
		jsonResult = json.load(data)

	result = json.JSONDecoder().decode(jsonResult)
	sleep(5)

def main():
	try:
		if len(sys.argv) == 3:
			data = sys.argv
			listFiles = os.listdir('Solutions')
			if data[1] not in listFiles:
				raise
			file = loadFile("Solutions/"+data[1])

			print len(file)
			if data[2] == 'True':
				folder = data[1]
			else:
				folder = None
			listOfSit = []
			try:
				solutions_drawn = '/media/vinicius/DATA/DrawingsAndGifs/' + folder
				dirs = os.listdir(solutions_drawn)
			except:
				dirs = []
			print dirs
			for s in file:
				if s['simName'] not in listOfSit:#and s['simName'] not in dirs:
					#print s.keys()
					#print s['solution']
					#'O092BVKS5B', 'XJWGEXNJZ0', 'DM9R0D4AEA', 'FQSTT3QCZI', 'P8E15OGTGM' diferentes
					if s['simName'] in ['A29AYUQDTZ']: #['O092BVKS5B', 'XJWGEXNJZ0', 'DM9R0D4AEA', 'FQSTT3QCZI', 'P8E15OGTGM', 'XBOBAEGQKR', 'BFL31065CL', 'V74WC6LNSZ', 'ZCCCDYF7QM', '3MLSASPZJ0', 'U8UFEXH40U', '4RJYSXXG7O']:#['BFL31065CL', 'U6P5N5O12J', 'A29AYUQDTZ', 'ZCCCDYF7QM', 'V74WC6LNSZ', '3MLSASPZJ0', 'XBOBAEGQKR', '4RJYSXXG7O','O092BVKS5B', 'XJWGEXNJZ0', '975IEQ6PY4', 'ABN9KJG55F', 'DM9R0D4AEA', 'FQSTT3QCZI', 'P8E15OGTGM', 'U8UFEXH40U', 'W2B2CUT2X4', 'X73VEUEWLS', 'DDZWTVA4IQ', 'DOR3KM2W1D', 'IRNW7EG9Z3', 'OV3U5M3WYI']:#'O092BVKS5B', 'XJWGEXNJZ0', 'DM9R0D4AEA', 'FQSTT3QCZI', 'P8E15OGTGM']: #'A29AYUQDTZ', 'U6P5N5O12J', 
					   show(s, folder)
					#raise
					listOfSit.append(s['simName'])
		else:
			raise
	except Exception as e:
		print e
		sys.exit()

if __name__ == '__main__':
	main()
		