import os
import pickle
import sys
try:
	sys.path.insert(0, '/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/Simulacao')
except:
	pass
try:
	sys.path.insert(0, '/home/ubuntu-gnome/Simulacao')
except:
	pass
import solveSituationsPyramid
import solveSituationsList
import constants

fileList = []

def loadFileList(directory):
	global fileList
	with open(directory, 'rb') as inputfile:
		files = pickle.load(inputfile)
		userPreferences =  files[len(files) - 1]
		fileList = iter(files[ : len(files) - 1])

def loadSituations():
	global fileList
	while True:
		try:
			file = next(fileList)
			solutionFile = file['file'].split('/')[-1]
			try:
				with open( solutionFile, 'rb') as inputfile:
					solutions = pickle.load(inputfile)
				for s in solutions:
					solution = solutions[s]['solution']
					if solution != None:
						if solution[0].score < 100000.0:
							solutions[s]['solution'] = None
							print "MUDANDO"
				with open(solutionFile, 'wb') as out:
					pickle.dump(solutions, out)
			except Exception as e:
				print e, file
			
		except:
			sys.exit()
def main():
	directory = os.getcwd().split('/')[-1]
	loadFileList(directory)
	loadSituations()

if __name__ == '__main__':
	main()

