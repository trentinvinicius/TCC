'''Join all solutions from a folder
	input: mainFileName, maximum difference for the solution be accepted
	output: file with all possible solutions for all the situations already solved
'''
import pickle
import sys
import os

def getFolders(key):
	dirs = os.listdir('Solutions')
	return [d for d in dirs if os.path.isdir('Solutions/' + d) and key in d]

def getFiles(mainFileName):
	with open(mainFileName, 'rb') as inputFile:
		mainFile = pickle.load(inputFile)
	fileList = [mainFile[i]['file'] for i in range(len(mainFile) - 1)]
	return fileList

def loadSolutions(fileList, maxDeviation):
	solutions = []	
	for f in fileList:
		with open(f, 'rb') as inputFile:
			file = pickle.load(inputFile)
		for s in file:
			situation= file[s]
			if situation['solution'] != None:
				solution = situation['solution']
				solutions.append({'simName': s, 'simData': situation['simData'], 'solution': solution[0].parameters, 'score': solution[0].score})
				for i, s2 in enumerate(solution):
					if i != 0 and s2.score != None:
						diff = solution[0].score - s2.score
						if diff < maxDeviation and not solution[0].parameters == s2.parameters:
							solutions.append({'simName': s, 'simData': situation['simData'], 'solution': s2.parameters, 'score': s2.score})
	return solutions

def main():
	try:
		data = sys.argv
		if len(data) != 3:
			raise
		else:
			_, key, maxDeviation = data
			dirs = getFolders(key)
			if not dirs:
				raise
			print len(dirs), " folder(s) found."
			totalSolutions = []
			for d in dirs:
				print ""
				print "#"*90	
				print "Folder ", d
				mainFileName = 'Solutions/' + d + '/' + d
				if os.path.isfile(mainFileName):
					fileList = getFiles(mainFileName)
					solutions = loadSolutions(fileList, maxDeviation)
					for s in solutions:
						totalSolutions.append(s)
			try:
				with open('Solutions/' + key, 'wb') as outputFile:
					pickle.dump(totalSolutions, outputFile)
			except:
				with open('Solutions/' + key + "joinedSolutions", 'wb') as outputFile:
					pickle.dump(totalSolutions, outputFile)
			print len(totalSolutions), " solutions saved."
	except Exception as e:
		print e
		print "Informe the mainFile name and the maximum difference for the solution be accepted"
		sys.exit()

if __name__ == '__main__':
	main()
