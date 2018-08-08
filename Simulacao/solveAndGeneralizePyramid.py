#from generalization import CNN
from solveSituationsPyramid import createName, callGA
from fixedSituationsNew import getSituations
import sys
import os
import pickle
import numpy as np
from multiprocessing import Process, Manager, cpu_count
from time import sleep
import itertools
import numpy as np
from constants import *
try:
	from sendEmail import createServer, sendEmail
except:
	pass


class Solver():
	def __init__(self, mainFileName):
		self.mainFileName = mainFileName
		self.simNumber = 0
		self.processesExecuted = 0
		self.processNum = 0
		self.processes = []
		self.simDict = Manager().dict()
		self.doneList = Manager().list()
		self.cpuInUse = np.zeros(cpu_count())
		self.savedSolutions = []
		self.pyramidStatus = {}
		self.IslandsPerSim = {}
		self.loadFileList()

	def loadFileList(self):
		with open(self.mainFileName, 'rb') as inputfile:
			self.files = pickle.load(inputfile)
			self.userPreferences = self.files[len(self.files) - 1]
			self.fileList = iter(self.files[ : len(self.files) - 1])

	def loadSituations(self):
		done = False
		try:
			while not done:
				file = next(self.fileList)
				if file['status'] == 0:
					#file['status'] = 1
					self.saveMainFile()
					self.solutionFile = file['file']
					with open(self.solutionFile, 'rb') as inputfile:
						self.solutions = pickle.load(inputfile)
					self.solutionsKeys = iter(self.solutions)
					done = True
			return False
		except:
			return True

	def getSituation(self):
		done = False
		while not done:
			try:
				simName = next(self.solutionsKeys)
				self.simNumber += 1
				#APENAS AQUI
				if self.solutions[simName]['solution'] == None:# or True:
					simData = self.solutions[simName]['simData']
					done = True
			except:
				done = self.loadSituations()
				if done == True:
					print "No more situaions to be loaded"
					return None
		return (simName, simData, self.solutionFile, self.simNumber)

	def saveSolutions(self):
		copy = dict(self.simDict)
		solutionsToBeSaved = [k for k, s in copy.iteritems() if s['optimumFound'].is_set() and k not in self.savedSolutions]
		for s in solutionsToBeSaved:
			simName = s
			print 'Saving ', s, '...'
			solutionFile = copy[s]['solutionFile']
			with open(solutionFile, 'rb') as inputfile:
				solutions = pickle.load(inputfile)
				solutions[simName]['solution'] = copy[s]['results'][0]
			with open(solutionFile, 'wb') as out:
				pickle.dump(solutions, out)
			try:
				sendEmail(solutionFile)
			except Exception as e:
				print ""
				print "Error sending email ", e
				print ""
			self.savedSolutions.append(simName)
			print '...done'


	def saveMainFile(self):
		with open(self.mainFileName, 'wb') as outputfile:
			pickle.dump(self.files, outputfile)

	def createProcesses(self):
		for k in range(1):
			data = self.getSituation()
			if data != None:
				simName, simData, solutionFile, simNumber = data
				islandsDone = Manager().Value('i', 0) # number of situations done
				statusSituation = Manager().Event() # if all situations are done, True
				results = Manager().list()
				optimumFound = Manager().Event()

				self.simDict[simName] = {'simData': simData, 'userPreferences': self.userPreferences, 'results': results, 'islandsDone': islandsDone, 'optimumFound': optimumFound, \
									     'statusSituation': statusSituation, 'solutionFile': solutionFile, 'simNumber': simNumber}		
				#debug
				self.IslandsPerSim[simName] = []
				#end debug
				for i in range(MAXISLANDSPYRAMID):
					j = simNumber * 7 + i
					#debug
					self.IslandsPerSim[simName].append(j)
					#end debug
					p = Process(target=callGA, args = (simName, simData, self.userPreferences, j, islandsDone, results, optimumFound, self.simDict, self.doneList, statusSituation, MAXISLANDSPYRAMID, ))
					self.processes.insert(0, {'process': p, 'simName': simName, 'island': j, 'CPU': None, 'status': 0}) # status: 0 ready 1 executing 2 stopped
					self.pyramidStatus[simName] = [0, 0] #[top, middle] 0 = not done, 1 = done
			else:
				return True
		return False

	def createPyramid(self, simDict, simName):
		j = max([p['island'] for p in self.processes if p['simName'] == simName])
		islandsDone = Manager().Value('i', 0) # number of situations done
	 	statusSituation = Manager().Event() # if all situations are done, True
		results = Manager().list()
		optimumFound = Manager().Event()

		inicialPopulation = []
		for r in simDict['results']:
			inicialPopulation += r
		try:
			simData = self.simDict[simName]['simData']
			solutionFile = self.simDict[simName]['solutionFile']
			simNumber = self.simDict[simName]['simNumber']
			self.simDict.pop(simName)
			self.simDict[simName] = {'simData': simData, 'userPreferences': self.userPreferences, 'results': results, 'islandsDone': islandsDone, \
			                         'optimumFound': optimumFound, 'statusSituation': statusSituation, 'solutionFile': solutionFile, 'simNumber': simNumber}	
		except Exception as e:
			print "Error: ", e
		for i in range(simDict['islandsDone'].value -1):
			p = Process(target=callGA, args = (simName, simDict['simData'], simDict['userPreferences'], j + 1 + i, islandsDone, results, optimumFound, self.simDict, self.doneList, statusSituation, simDict['islandsDone'].value-1, inicialPopulation, ))
			#debug
			self.IslandsPerSim[simName].append(j + 1 + i)
			#end debug
			self.processes.insert(0, {'process': p, 'simName': simName, 'island': j + 1 + i, 'CPU': None, 'status': 0}) # status: 0 ready 1 executing 2 stopped
			#debug
			print 'New Process: ', {'process': p, 'simName': simName, 'island': j + 1 + i, 'CPU': None, 'status': 0}
			#end debug

	def killProcesses(self, simName, island = None):
		filesToDelete = []
		if island == None:
			processes = [p for p in self.processes if p['simName'] == simName and p['status'] <= 1]
			for p in processes:
				filesToDelete.append('jsonParamaters' + str(p['island']) + '.txt')
				filesToDelete.append('fitness' + str(p['island']) + '.txt') 
		else:
			processes = [item for item in self.processes if item['simName'] == simName and item['island'] == island]
		print "FINISHING..."
		for p in processes:
			print p
			try:
				p['process'].terminate()
				p['process'].join()
				p['status']  = 2
			except Exception as e:
				print "Error killing process ", e
			self.cpuInUse[p['CPU']] = 0

		sleep(10)
		try:
			for f in filesToDelete:
				os.remove(f)
		except Exception as e:
			print "Error ", e

	def addNewProcesses(self, atTheEnd = False):
		for i, c in enumerate(self.cpuInUse):
			if atTheEnd:
				"check if the process has not yet been executed"
				condition = c == 0 and self.processes[0]['status'] == 0
			else:
				condition = c == 0
			if condition:
				processToExecute = self.processes[0]
				self.processes.append(self.processes.pop(0))
				self.processNum += 1
				processToExecute['CPU'] = i
				processToExecute['status'] = 1
				processToExecute['process'].start()
				pid = processToExecute['process'].pid
				self.cpuInUse[i] = pid
				os.system("taskset -p -c %d %d" % (i , pid))

	def step(self):
		#wait until a process has finished
		while len(self.doneList) < self.processesExecuted:
			pass
		#check if there is any solution to be saved
		self.saveSolutions()
		#kill all the processes that have finished
		while self.processesExecuted < len(self.doneList):
			processDone = self.doneList[self.processesExecuted] #[simName, island]
			self.processesExecuted += 1
			#if the optimum value or all the island are done, kill them all or just kill the processs
			if self.simDict[processDone[0]]['optimumFound'].is_set(): #or islands
				self.killProcesses(processDone[0])
			else:
				self.killProcesses(processDone[0], processDone[1])
			try:
				if self.simDict[processDone[0]]['statusSituation'].is_set() and self.simDict[processDone[0]]['islandsDone'].value > 1:
					if (self.pyramidStatus[processDone[0]][self.simDict[processDone[0]]['islandsDone'].value - 2]  == 0):
						self.pyramidStatus[processDone[0]][self.simDict[processDone[0]]['islandsDone'].value - 2] = 1
						self.createPyramid(self.simDict[processDone[0]], processDone[0])
			except Exception as e:
				print "Error ", e

	def run(self):
		try:
			done = False
			while not done:
				try:
					#wait until a cpu is avaliable
					while not 0 in self.cpuInUse:
						self.step()

					#add the next process to next available cpu
					self.addNewProcesses()

				except KeyboardInterrupt:
					sim = dict(self.simDict)
					for s in sim:
						self.killProcesses(s)
				except:
					#if there is no more processes in the list, try adding more
					done = self.createProcesses()
			#wait all processes to be done 
			while sum(self.cpuInUse) > 0: # or True:
				self.step()
				self.addNewProcesses(True)
				#debug
				#print sum(self.cpuInUse), self.cpuInUse
				#print len(self.savedSolutions)
				#end debug
			print "ENDING"
		except Exception as e:
			print(e)

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
		filename = 'Solutions/' + info[1] + '/' + info[1]
		s = Solver(filename)
		s.run()
	else:
		try:
			if len(info) == 4:
				_, username, userPreferencesFilename, number = info
				try:
					try:
						os.mkdir('Solutions/' + username)
					except:
						pass
					with open('userPreferences/' + userPreferencesFilename, 'rb') as inputfile:
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
								#vector[13] = u
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


					"for just create the situations file"
					sys.exit()


					print "Starting GA..."
					filename = 'Solutions/' + username + '/' + username
					s = Solver(filename)
					s.run()
				except Exception as e:
					exc_type, exc_obj, exc_tb = sys.exc_info()
					fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
					print exc_type, fname, exc_tb.tb_lineno
					print e
					print "Problem loading/saving file"
					raise

			else:
				print "Informe username, filename with user preferences and the number of situations to be solved"
				raise
		except:
			sys.exit()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		print "END"
"""sim = dict(self.simDict)
		for s in sim:
			self.killProcesses(s)"""
