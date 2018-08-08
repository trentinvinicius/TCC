#from generalization import CNN
from solveSituationsNew import createProcesses, killProcesses, createName
from fixedSituationsNew import getSituations
import sys
import os
import pickle
import numpy as np
from multiprocessing import Process, Manager
from time import sleep


#processes = {}

def runSituation(simulationData, simName, userPreferences, oneIslandPerCPU, simFile, fileList, filename, simExecuting, wait, maxSimExecuting, situationNum, save):
	simExecuting.value += 1
	#situationNum.value += 1
	print "Starting situation: ", situationNum.value
	if simExecuting.value == maxSimExecuting:
		wait.set()
	try:
		result = createProcesses(simName, simulationData, userPreferences, situationNum, oneIslandPerCPU) #% maxSimExecuting
	except KeyboardInterrupt:
		killProcesses()
		simFile['status'] = 0
		with open(filename, 'wb') as outputfile:
			pickle.dump(fileList, outputfile)
		sys.exit()
	except:
		result = None
	try:
		while save.is_set():
			pass
		save.set()
		with open(simFile['file'], 'rb') as inputfile:
			solutions = pickle.load(inputfile)
			solutions[simName]['solution'] = result
		with open(simFile['file'], 'wb') as out:
			pickle.dump(solutions, out)
		save.clear()
	except:
		pass
	simExecuting.value -= 1
	#killProcess(simName)
	if simExecuting.value == maxSimExecuting - 1:
		wait.clear()

def killProcess(simName):
	global processes
	print processes
	print simName
	processes[simName].terminate()
	processes[simName].join()

def runSolveSituations(username, maxSimExecuting, oneIslandPerCPU):
	#global processes
	situationNum = 0
	filename = 'Solutions/' + username + '/' + username
	with open(filename, 'rb') as inputfile:
		fileList = pickle.load(inputfile)
	userPreferences = fileList[len(fileList) - 1]
	with Manager() as manager:
		simExecuting = manager.Value('i', 0)
		#situationNum = manager.Value('i', 0)
		wait = manager.Event()
		save = manager.Event()
		for i in range(len(fileList)- 1):
			simFile = fileList[i]
			if simFile['status'] == 0:
				simFile['status'] = 1
				with open(filename, 'wb') as outputfile:
					pickle.dump(fileList, outputfile)				
				with open(simFile['file'], 'rb') as inputfile:
					solutions = pickle.load(inputfile)
				for key, value in solutions.iteritems():
					situationNum += 1
					if value['solution'] == None:
						simulationData = value['simData']
						simName = key
						print simName
						p = Process(target=runSituation, args = (simulationData, simName, userPreferences, oneIslandPerCPU, simFile, fileList, filename, simExecuting, wait, maxSimExecuting, situationNum, save, ))
						p.start()
						#processes[simName] = p
					sleep(10)
					while wait.is_set(): 	
						pass					
			simFile['status'] = 2
			with open(filename, 'wb') as outputfile:
				pickle.dump(fileList, outputfile)

def main():
	'''
	info: 
		* username
		* filename where there are the user preferences dictionary 
			and the percentual vector for the selection of the situations
		* number of situations to be solved
	'''
	info = sys.argv
	listFiles = os.listdir('Solutions')

	if info[1] in listFiles and os.path.isfile('Solutions/' + info[1] + '/' + info[1]):
		print "Starting GA..."
		runSolveSituations(info[1], int(info[2]), True if info[3] == '1' else False)
	else:
		try:
			if len(info) == 6:
				_, username, maxSimExecuting, oneIslandPerCPU, filename, number = info
				try:
					try:
						os.mkdir('Solutions/' + username)
					except:
						pass
					with open('userPreferences/' + filename, 'rb') as inputfile:
						preferencesAndVector = pickle.load(inputfile)
					userPreferences = preferencesAndVector['userPreferences']
					userVector	    = preferencesAndVector['userVector']
					mainFile = []
					print "Loading situations..."
					for i, u in enumerate(userVector):
						if u > 0:
							name = 'Solutions/' + username + '/' + username + str(i)
							if not os.path.isfile(name):
								vector = np.zeros(14)
								vector[i] = u
								simData = getSituations(int(number), vector)
								solutions = {}
								for sData in simData:
									simName = createName()
									solutions[simName] = {'simData' : sData, 'solution' : None}
								with open(name, 'wb') as outputfile:
									pickle.dump(solutions, outputfile)
							dic = {'file': name, 'status': 0} # 0 not done, 1 started, 2 finished
							mainFile.append(dic)
					mainFile.append(userPreferences)
					print "...done"
					with open('Solutions/' + username + '/' + username, 'wb') as outputfile:
						pickle.dump(mainFile, outputfile)
					print "Starting GA..."
					runSolveSituations(username, int(maxSimExecuting), True if oneIslandPerCPU == '1' else False)
				except Exception as e:
					print(e)
					print "Problem loading/saving file"
					raise
			else:
				print "Informe username, number of simultaneously simulation executing (1 or 2), one Island per CPU (0 or 1), filename with user preferences and the number of situations to be solved"
				raise
		except:
			sys.exit()


if __name__ == '__main__':
	main()