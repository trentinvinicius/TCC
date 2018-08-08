import sys
import pickle
import os
import json


def loadFile(mainFileName):
	with open(mainFileName, 'rb') as inputFile:
		mainFile = pickle.load(inputFile)
	return mainFile


def show(s, color):
	FILEWRITE = 'jsonParamaters.txt'
	FILEREAD = 'fitness.txt'
	mc, r, oc, p, a, tp, river = s['simData']

	#if s['simName'] == 'IYMZ2X7OC3':

	msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
		   "animalInfo": a, "riverInfo": river, "parameters": s['solution'], "name": s['simName'], "test" : False, "visualization" : True, "color" : color}
    
	jsonSim = json.JSONEncoder().encode(msg)

	with open(FILEWRITE, 'w') as outfile:
		json.dump(jsonSim, outfile)

	call = 'python callSim.py'
	os.system(call)
	with open(FILEREAD) as data:
		jsonResult = json.load(data)

	result = json.JSONDecoder().decode(jsonResult)

	collisions, inRiver, out, minDist = result
	print "Collisions: ", collisions
	
	

	"""
	msg = {"mainCarInfo": mc, "roadInfo": r, "peopleInfo": p, "otherCarsInfo": oc, "treepoleInfo": tp, \
		   "animalInfo": a, "riverInfo": river, "parameters": s['solution'], "name": s['simName'], "test" : False, "visualization" : False, "color" : color}
    
	jsonSim = json.JSONEncoder().encode(msg)

	with open(FILEWRITE, 'w') as outfile:
		json.dump(jsonSim, outfile)

	call = 'python callSim.py'
	os.system(call)
	with open(FILEREAD) as data:
		jsonResult = json.load(data)

	result = json.JSONDecoder().decode(jsonResult)

	collisions, inRiver, out, minDist = result
	print "Collisions: ", collisions"""

def main():
	try:
		info = sys.argv
		if len(info) == 3:
			_, filename1, filename2 = info
		else:
			print "Informe the name from the files to be compared"
			raise
		listFiles = os.listdir('Solutions')
		if ((filename1 not in listFiles) and (filename2 not in listFiles)):
			raise		
		file1 = loadFile("Solutions/"+filename1)
		file2 = loadFile("Solutions/"+filename2)
		listOfSit = []
		for s1 in file1:
			i = 0
			if s1['simName'] not in listOfSit:
				for s2 in file2:
					#print s1['simName'], s2['simName']
					if s2['simName'] == s1['simName'] and i < 1:

						mc, r, oc, p, a, tp, river = s1['simData']

						if r[4] == 1:

							print "#"*70
							print "The situation ", s1['simName'], " was found in both files"
							#print s1.keys()
							print "Score file1: ", s1['score']
							print "Score file2: ", s2['score']
							#if s1['simName'] in ['8HNPMP57TD', '01PGF3X0XJ', '9BSE1ITIL5', '8HNPMP57TD', 'BFL31065CL', '3MLSASPZJ0', '9DXKJKV72G', 'ZIT099L427']:
							#show(s1, 0)
							#show(s2, 1)
							i += 1
							"""if s1['simName'] == "IYMZ2X7OC3":
																									raise"""
				listOfSit.append(s1['simName'])
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		print exc_type, fname, exc_tb.tb_lineno
		sys.exit()

if __name__ == '__main__':
	main()