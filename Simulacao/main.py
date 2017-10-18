from simulation import Sim
from math import pi 
from genetic import GeneticAlgorithm

mainCarInfo = (5, 100, 0)
roadInfo = (4, 1, 2)
peopleInfo = [((-0, 0, 7), (0, 0, 0))]
treepoleInfo = [(10, 0, 1), (15, 0, 0), (12, 1, 1), (18, 1, 0), (21, 0, 1), (24, 0, 1), (27, 0, 0), (30, 0, 0)]
otherCarsInfo = [((7, 0, -3), -1, 0), ((17, 0, -3), -1, 0)]
parameters = [-0, 1, 1, pi/2]
#print "A"
sim = Sim(mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo = otherCarsInfo, treepoleInfo = treepoleInfo)
#print "A"
sim.start()
#print "A"
print sim.getFitness()
