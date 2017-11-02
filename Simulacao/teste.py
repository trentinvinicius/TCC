from multiprocessing import Process, Queue
from simulation import Sim
from math import pi 
from genetic import GeneticAlgorithm
import gc

mainCarInfo = (5, 200, 0)
roadInfo = (4, 1, 2)
peopleInfo = [((-0, 0, 7), (0, 0, 0))]
treepoleInfo = [(10, 0, 1), (15, 0, 0), (12, 1, 1), (18, 1, 0), (21, 0, 1), (24, 0, 1), (27, 0, 0), (30, 0, 0)]
otherCarsInfo = [((7, 0, -3), -1, 10), ((17, 0, -3), -1, 10)]
parameters = [-0, 1, 1, pi/2]

def f(mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo):
    sim = Sim(mainCarInfo, roadInfo, peopleInfo, parameters,'A', otherCarsInfo = otherCarsInfo, treepoleInfo = treepoleInfo)
    sim.start()
    print "ABc"
    return 0
if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo,))
    p.start()
    fa = Process(target=f, args=(mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo,)) 	
    #p.start()
    fa.start()

for i in range(100):
	while():
		