#from generalization import CNN
from solveSituationsList import createName, callGA
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
				if file['status'] == 0 or True:
					#file['status'] = 1
					self.saveMainFile()
					self.solutionFile = file['file']
					with open(self.solutionFile, 'rb') as inputfile:
						self.solutions = pickle.load(inputfile)
					self.solutionsKeys = iter(self.solutions)
					done = True
			return False
		except:
			print "Terminou"
			return True

	def getSituation(self):
		done = False
		while not done:
			try:
				simName = next(self.solutionsKeys)
				self.simNumber += 1
				#APENAS AQUI
				if self.solutions[simName]['solution'] == None or True:

					simData = self.solutions[simName]['simData']
					done = True
			except:
				done = self.loadSituations()
				if done == True:
					return None
		return (simName, simData, self.solutionFile, self.simNumber)

	def saveSolutions(self):
		copy = dict(self.simDict)
		solutionsToBeSaved = [k for k, s in copy.iteritems() if s['optimumFound'].is_set() and k not in self.savedSolutions]# s['saved'] == False]
		for s in solutionsToBeSaved:
			simName = s
			print "Saving ", s, '...'
			#result = max(copy[s]['results'], key=lambda r: r['score'])['parameters']
			solutionFile = copy[s]['solutionFile']
			with open(solutionFile, 'rb') as inputfile:
				solutions = pickle.load(inputfile)
				aux = []
				for c in copy[s]['results']:
					for s in c:
						aux.append(s)
				try:
					solutions[simName]['solution'] = aux#copy[s]['results'] #result
					self.savedSolutions.append(simName)
				except Exception as e:
					print "Error saving: ", e

			with open(solutionFile, 'wb') as out:
				pickle.dump(solutions, out)
			self.simDict[simName]['saved'] = True
			copy[simName]['saved'] = True

	def saveMainFile(self):
		with open(self.mainFileName, 'wb') as outputfile:
			pickle.dump(self.files, outputfile)

	def createProcesses(self):
		'''with Manager() as manager:
												self.simDict = manager.dict()
												self.doneList = manager.list()'''			
		islandsDone = 0
		optimumFound = False
		results = []
		saved = False

		for k in range(1):
			data = self.getSituation()
			if data != None:
				simName, simData, solutionFile, simNumber = data
				islandsDone = Manager().Value('i', 0)
				results = Manager().list()
				optimumFound = Manager().Event()
				self.simDict[simName] = {'results': results, 'islandsDone': islandsDone, 'optimumFound': optimumFound,\
									'solutionFile': solutionFile, 'simNumber': simNumber, 'saved': saved}		
				pList = [] # list with the process from this simulation
				for i in range(MAXISLANDSLIST):
					j = simNumber * MAXISLANDSLIST + i
					p = Process(target=callGA, args = (simName, simData, self.userPreferences, j, islandsDone, results, optimumFound, self.simDict, self.doneList,  ))
					self.processes.append({'process': p, 'simName': simName, 'island': j, 'CPU': None, 'status' : 0}) # 0 ready 1 executing 2 stopped
				#self.processes = itertools.chain(self.processes, pList)
			else:
				return True
		return False

	def killProcesses(self, simName, island = None):
		filesToDelete = []
		if island == None:
			processes = [p for p in self.processes if p['simName'] == simName and p['status'] <= 1]
			simNumber = self.simDict[simName]['simNumber']
			for i in range(MAXISLANDSLIST):
				j = simNumber * MAXISLANDSLIST + i
				filesToDelete.append('jsonParamaters' + str(j) + '.txt')
				filesToDelete.append('fitness' + str(j) + '.txt') 
		else:
			processes = [item for item in self.processes if item['simName'] == simName and item['island'] == island]
		for p in processes:
			print "Finishing ", p, "..."
			p['process'].terminate()
			p['process'].join()
			p['status']  = 2
			self.cpuInUse[p['CPU']] = 0
		sleep(10)
		try:
			for f in filesToDelete:
				os.remove(f)
		except Exception as e:
			print "ERROR ", e

	def run(self):
		try:
			done = False
			while not done:
				try:
					#wait until a cpu is avaliable
					while not 0 in self.cpuInUse:
						#wait until a process has finished
						while len(self.doneList) <= self.processesExecuted:
							pass
						#check if there is any solution to be saved
						self.saveSolutions()
						#kill all the processes that have finished
						while self.processesExecuted < len(self.doneList):
							processDone = self.doneList[self.processesExecuted]
							self.processesExecuted += 1
							#debug
							print processDone, self.doneList
							print [item for item in self.processes if item['simName'] == processDone[0] and item['island'] == processDone[1]]
							#if the optimum value or all the island are done, kill them all or just kill the processs
							if self.simDict[processDone[0]]['optimumFound'].is_set():
								self.killProcesses(processDone[0])
							else:
								self.killProcesses(processDone[0], processDone[1])
					#add the next process to next available cpu
					for i, c in enumerate(self.cpuInUse):
						if c == 0:
							processToExecute = self.processes[self.processNum]
							self.processNum += 1
							processToExecute['CPU'] = i
							processToExecute['status'] = 1
							processToExecute['process'].start()
							pid = processToExecute['process'].pid
							self.cpuInUse[i] = pid
							os.system("taskset -p -c %d %d" % (i , pid))
				except:
					#if there is no more processes in the list, try adding more
					done = self.createProcesses()
			#wait all processes to be done 
			while sum(self.cpuInUse) > 0:
				while len(self.doneList) <= self.processesExecuted:
					pass
				processDone = self.doneList[self.processesExecuted]
				if self.simDict[processDone[0]]['optimumFound'].is_set(): #self.simDict[processDone[0]]['islandsDone'] == MAXISLANDSLIST or 
					self.killProcesses(processDone[0])
				else:
					self.killProcesses(processDone[0], processDone[1])
				self.saveSolutions()
				self.processesExecuted += 1
			print "ENDING"
		except KeyboardInterrupt:
			sim = dict(self.simDict)
			for s in sim:
				print s
				self.killProcesses(s)
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
	main()