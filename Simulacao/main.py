from simulation import Sim
    
mainCarInfo = (5, 10, 0)
roadInfo = (4, 1, 2)
peopleInfo = [((-0, 0, -7), (10, 0, 5)), ((20, 0, 20), (-15, 0, 1))]
treepoleInfo = [(10, 0, 1), (15, 0, 0), (12, 1, 1), (18, 1, 0)]
otherCarsInfo = [((20, 0, -3), 1, 20)]

sim = Sim(mainCarInfo, roadInfo, peopleInfo, otherCarsInfo = otherCarsInfo, treepoleInfo = treepoleInfo)
sim.start()
