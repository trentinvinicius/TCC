import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin, sqrt, acos, asin
import numpy as np
from objects import *
from constants import *
from operator import itemgetter
import json
from time import sleep
import os
import pickle
#import pylab as plt
import matplotlib.pyplot as plt
from createImages import createImages

class Sim(ode_viz.ODE_Visualization):
  def __init__(self, mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo, animalInfo, riverInfo, name, test, visualization, colorMainCar = 0, folderToSave = None, drawTrajectory = False):
    self.iniciate()
    self.createWorld()
    self.mainCarInfo = mainCarInfo        # (numPassengers, velocity, inicialSteerAngle)
    self.mainCarVelocity = self.mainCarInfo[1]
    self.roadInfo = roadInfo              # (nLanes, direction, position mainCar, crosswalk position, status semaphore)
    self.peopleInfo = peopleInfo          # [(position, velocity, gender, age, num)], position = x, z, theta
    self.otherCarsInfo = otherCarsInfo    # [(position, direction, velocity, num)], position = x, 0, z
    self.treepoleInfo = treepoleInfo      # [(x, z, tree, num)], z is 0 or 1 corresponding the side of the road, tree is 0 or 1: 0 - pole, 1 - tree
    self.animalInfo = animalInfo          # [(position, velocity, num)]
    self.riverInfo = riverInfo            # [True or False, position]
    self.parameters = parameters          # parameters from the genetic algorithm
    self.calcSteerAngles()
    if visualization:
      ode_viz.ODE_Visualization.__init__(self, self.world, [self.space], TIMESTEP)
      self.visualization = self
      self.space = self.space[0]
    else:
      self.visualization = False
    self.colorMainCar = colorMainCar
    self.drawTrajectory = drawTrajectory
    if folderToSave != None:
      dirs = os.listdir('/media/vinicius/DATA/DrawingsAndGifs')#('Solutions/DrawingsAndGifs')
      folders = [d for d in dirs if os.path.isdir('/media/vinicius/DATA/DrawingsAndGifs' + d)]
      self.folderToSave = '/media/vinicius/DATA/DrawingsAndGifs/' + folderToSave
      if folderToSave not in folders:
        call1 = 'mkdir ' + self.folderToSave
      else:
        call1 = ''
      self.folderToSave += '/' + name
      call2 = 'mkdir ' + self.folderToSave
      #print call1, call2
      if self.drawTrajectory == False:
        os.system(call1)
        os.system(call2)
        comand = 'mkdir ' + self.folderToSave + '/imagesNN'
        os.system(comand)
    else:
      self.folderToSave = folderToSave

    self.drawTrajectory = drawTrajectory
    self.paramToCall = mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo, animalInfo, riverInfo, name, test, visualization, colorMainCar, folderToSave, True

    if self.drawTrajectory:
      self.trajectory()
      self.auxImageCreator = 0
      self.createImagesNN()

    self.otherCars = []
    self.people = []
    self.animal = []
    self.treepole = []
    self.createBase()
    self.updateDistances()
    self.createObjects()
    self.cameraFocalPoint = np.array(self.mainCar.getPosition()) + (10, 0, 0) #- (ROADLENGTH/2 - 100.0, 0, 0)
    self.cameraPosition = np.array(self.cameraFocalPoint) - (50, -30, 0)   
    if self.visualization:
      self.changeCameraPosition()
      self.SetSize(WINDOWSIZE[0], WINDOWSIZE[1])
      title = "Simulation " + str(name)
      self.SetWindowName(title)
      self.SetBackground(50./255, 153./255, 204./255)
    self.auxBrake = True
    self.simName = name
    self.test = test
    self.stopCriteria = False
    self.fitness = None
    if self.test:
      self.collisions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 1000]
    else:
      self.collisions = []
    self.enableSteer = False
    self.auxTest = True
    self.mySimulationTime = 0
    self.distAuxCar = [1000, 0]
    self.distAuxCross = 1000
    self.mainCarPositions = []
    self.startBrakeandSteer = MAXSIMTIME
    self.inRiver = []
    self.auxReduceVelocity = True
    self.auxNumImg = 0

    self.contactgroup = ode.JointGroup()

  def createBase(self):
    #create a plane geom which prevent the objects from falling forever
    self.floor = ode.GeomPlane(self.space, (0, 1, 0), 0)
    if self.visualization:
      self.addGeom(self.floor)
    self.floor.__setattr__('name','Floor')

    numLanes, _, laneMain, _, _  = self.roadInfo
    if (laneMain <= numLanes/2.0):
      zPos = -(numLanes/2.0 - laneMain + 0.5) * ROADSIZE
    else:
      zPos = (laneMain - numLanes/2.0 -1 + 0.5) * ROADSIZE
    self.topBasePos, self.bottomBasePos = zPos + numLanes/2.0 * ROADSIZE + BASEWIDTH/4, zPos - numLanes/2.0 * ROADSIZE - BASEWIDTH/4

    #create a base 
    if self.riverInfo[0]:
      self.geomBase1 = ode.GeomBox(self.space, (BASELENGTH/2, BASEHEIGHT, BASEWIDTH/2))
      self.geomBase1.setPosition((self.riverInfo[1] + RIVERSIZE/2 + BASELENGTH/4, BASEHEIGHT/2, self.topBasePos))
      self.fxJoint1 = ode.FixedJoint(self.world)
      self.fxJoint1.attach(self.geomBase1.getBody(), ode.environment)
      self.fxJoint1.setFixed()
      self.geomBase2 = ode.GeomBox(self.space, (BASELENGTH/2, BASEHEIGHT, BASEWIDTH/2))
      self.geomBase2.setPosition((self.riverInfo[1] - RIVERSIZE/2 - BASELENGTH/4, BASEHEIGHT/2, self.topBasePos))
      self.fxJoint2 = ode.FixedJoint(self.world)
      self.fxJoint2.attach(self.geomBase2.getBody(), ode.environment)
      self.fxJoint2.setFixed()
      self.geomBase3 = ode.GeomBox(self.space, (BASELENGTH/2, BASEHEIGHT, BASEWIDTH/2))
      self.geomBase3.setPosition((self.riverInfo[1] + RIVERSIZE/2 + BASELENGTH/4, BASEHEIGHT/2, self.bottomBasePos))
      self.fxJoint3 = ode.FixedJoint(self.world)
      self.fxJoint3.attach(self.geomBase1.getBody(), ode.environment)
      self.fxJoint3.setFixed()
      self.geomBase4 = ode.GeomBox(self.space, (BASELENGTH/2, BASEHEIGHT, BASEWIDTH/2))
      self.geomBase4.setPosition((self.riverInfo[1] - RIVERSIZE/2 - BASELENGTH/4, BASEHEIGHT/2, self.bottomBasePos))
      self.fxJoint4 = ode.FixedJoint(self.world)
      self.fxJoint4.attach(self.geomBase2.getBody(), ode.environment)
      self.fxJoint4.setFixed()

      if self.visualization:
        self.addGeom(self.geomBase1)
        self.addGeom(self.geomBase2)
        self.addGeom(self.geomBase3)
        self.addGeom(self.geomBase4)
        self.GetObject(self.geomBase1).SetTexture('Images/floor.jpeg')
        self.GetObject(self.geomBase2).SetTexture('Images/floor.jpeg')
        self.GetObject(self.geomBase3).SetTexture('Images/floor.jpeg') 
        self.GetObject(self.geomBase4).SetTexture('Images/floor.jpeg')
      self.geomBase1.__setattr__('name','Base')
      self.geomBase2.__setattr__('name','Base')
      self.geomBase3.__setattr__('name','Base')
      self.geomBase4.__setattr__('name','Base')
    else:
      self.geomBase1 = ode.GeomBox(self.space, (BASELENGTH, BASEHEIGHT, BASEWIDTH/2))
      self.geomBase1.setPosition((BASELENGTH/2 - 500.0, BASEHEIGHT/2, self.topBasePos))
      self.fxJoint1 = ode.FixedJoint(self.world)
      self.fxJoint1.attach(self.geomBase1.getBody(), ode.environment)
      self.fxJoint1.setFixed()
      self.geomBase2 = ode.GeomBox(self.space, (BASELENGTH, BASEHEIGHT, BASEWIDTH/2))
      self.geomBase2.setPosition((BASELENGTH/2 - 500.0, BASEHEIGHT/2, self.bottomBasePos))
      self.fxJoint2 = ode.FixedJoint(self.world)
      self.fxJoint2.attach(self.geomBase2.getBody(), ode.environment)
      self.fxJoint2.setFixed()
      if self.visualization:
        self.addGeom(self.geomBase1)
        self.addGeom(self.geomBase2)
        self.GetObject(self.geomBase1).SetTexture('Images/floor.jpeg')
        self.GetObject(self.geomBase2).SetTexture('Images/floor.jpeg')
      self.geomBase1.__setattr__('name','Base')
      self.geomBase2.__setattr__('name','Base')

  def createWorld(self):
    #create world
    self.world = ode.World()
    self.world.setGravity(GRAVITY)
    self.world.setERP(0.8)
    self.world.setCFM(1E-5)
    #create Space
    self.space = ode.Space()

  def updateDistances(self):
    #opening files with the information needed to 'delay' the simulation
    with open('animalvelocity.txt') as data:
      animalvelocity = json.load(data)
    with open('peoplevelocity.txt') as data:
      peoplevelocity = json.load(data)
    with open('velocTimeDist.txt') as data:
      velDistTime = json.load(data)

    #vectors that hold the information from the files
    tempos          =     []
    distancia       =     []
    vel             =     []
    animaltempos    =     []
    animaldistancia =     []
    animalvel       =     []
    peopletempos    =     []
    peopledistancia =     []
    peoplevel       =     []

    for vdt in velDistTime:
      vel.append(vdt[0])
      tempos.append(vdt[1][0])
      distancia.append(vdt[1][1])

    for avdt in animalvelocity:
      animalvel.append(avdt[0])
      animaldistancia.append(avdt[1])
      animaltempos.append(avdt[2])

    for pvdt in peoplevelocity:
      peoplevel.append(pvdt[0])
      peopledistancia.append(pvdt[1])
      peopletempos.append(pvdt[2])

    tempoGeral = []

    passangerNum, velocity, steerAngle = self.mainCarInfo
    velId = [i for i, x in enumerate(vel) if x >= velocity][0]
    dist = (distancia[velId] - distancia[velId - 1])*(velocity - vel[velId]) + distancia[velId]
    tempo = (tempos[velId] - tempos[velId - 1])*(velocity - vel[velId]) + tempos[velId]
    steerAngle = 0.0
    tempoGeral.append(tempo)
    self.mainCarInfo = [passangerNum, velocity, steerAngle, dist, tempo]

    if self.otherCarsInfo != None:
      newOtherCarsInfo = []
      for oc in self.otherCarsInfo:
        pos, direction, velocity, j = oc
        velId = [k for k, v in enumerate(vel) if v >= velocity][0]
        dist = (distancia[velId] - distancia[velId - 1])*(velocity - vel[velId]) + distancia[velId]
        tempo = (tempos[velId] - tempos[velId - 1])*(velocity - vel[velId]) + tempos[velId]
        tempoGeral.append(tempo)
        newOtherCarsInfo.append([pos, direction, velocity, dist, tempo, j])
        self.otherCarsInfo = newOtherCarsInfo

    if self.peopleInfo != None:
      newPeopleInfo = []
      for p in self.peopleInfo:
        pos, v, o, gender, age, j = p
        velId = [k for k, pv in enumerate(peoplevel) if pv >= v][0]
        dist = (peopledistancia[velId] - peopledistancia[velId - 1])*(v - peoplevel[velId]) + peopledistancia[velId]
        tempo = (peopletempos[velId] - peopletempos[velId - 1])*(v - peoplevel[velId]) + peopletempos[velId]
        tempoGeral.append(tempo)
        newPeopleInfo.append([pos, v, o, dist, tempo, gender, age, j])
      self.peopleInfo = newPeopleInfo

    if self.animalInfo != None:
      newAnimalInfo = []
      for a in self.animalInfo:
        pos, v, o, j = a
        velId = [k for k, av in enumerate(animalvel) if av >= v][0]
        dist = (animaldistancia[velId] - animaldistancia[velId - 1])*(v - animalvel[velId]) + animaldistancia[velId]
        tempo = (animaltempos[velId] - animaltempos[velId - 1])*(v - animalvel[velId]) + animaltempos[velId]
        tempoGeral.append(tempo)
        newAnimalInfo.append([pos, v, o, dist, tempo, j])
      self.animalInfo = newAnimalInfo

    #update distances according to the maximum time 
    maxTime = max(tempoGeral)
    self.mainCarInfo[3] += self.mainCarInfo[1]*(maxTime - self.mainCarInfo[4])
    if self.otherCarsInfo != None:
      for oc in self.otherCarsInfo:
        oc[3] += oc[2]*(maxTime - oc[4])

    if self.peopleInfo != None:
      newPeopleData = []
      for p in self.peopleInfo:
        p[3] += p[1]*(maxTime - p[4])
        ang = (p[2] - 180)*pi/180
        x, _, z = p[0]
        x += p[3]*cos(ang)
        z -= p[3]*sin(ang)
        newPeopleData.append([(x, 0, z), p[1], p[2], p[5], p[6], p[7]])
      self.peopleInfo = newPeopleData

    if self.animalInfo != None:
      newAnimalData = []
      for a in self.animalInfo:
        a[3] += a[1]*(maxTime - a[4])
        ang = (a[2] - 180)*pi/180
        x, _, z = a[0]
        x += a[3]*cos(ang)
        z -= a[3]*sin(ang)
        newAnimalData.append([(x, 0, z), a[1], a[2], a[5]])
      self.animalInfo = newAnimalData

  def createObjects(self):
    #numLanes, direction, laneMain, crossPos, statusSemaphore
    self.road = Road(self.world, self.space, self.visualization, self.roadInfo[0], self.roadInfo[1], self.roadInfo[2], self.roadInfo[3], self.roadInfo[4])
    if self.riverInfo[0]:
      self.bridge = Bridge(self.world, self.space, self.visualization, self.riverInfo[1], self.road.getSides())
    #dist, passengers
    self.mainCar = Car(self.world, self.space, self.visualization, self.mainCarInfo[3], passengers = self.mainCarInfo[0], color = self.colorMainCar) 
    sideTop, sideBottom = self.road.getSides()
    if (self.treepoleInfo != None):
       for tp in self.treepoleInfo:
          if tp[1] == 0:
             s = sideTop + 1
          else:
             s = sideBottom - 1
          #position, tree, num
          if not (tp[1] == 0 and (self.roadInfo[3] - 10 < tp[0] < self.roadInfo[3] + 3) and self.roadInfo[3] > 0):
            teste = TreePole(self.world, self.space, self.visualization, (tp[0], 0, s), tp[2], tp[3])
            self.treepole.append(teste)
    if (self.peopleInfo != None):
       for p in self.peopleInfo:
          #position, velocity, orientation, gender, age, num
          self.people.append(Person(self.world, self.space, self.visualization, p[0], p[1], p[2], p[3], p[4], p[5]))
    if (self.animalInfo != None):
        for a in self.animalInfo:
          #position, velocity, orientation, num
          self.animal.append(Animal(self.world, self.space, self.visualization, a[0], a[1], a[2], a[3]))
    if (self.otherCarsInfo != None):
       for c in self.otherCarsInfo:
          car = Car(self.world, self.space, self.visualization, c[3], mainCar = False, position = c[0], direction = c[1], num = c[5])
          car.setLinearVelocity(c[2])
          car.setSteerAngle(0.0)
          self.otherCars.append((car, c[2]))
    self.mainCar.setSteerAngle(self.mainCarInfo[2])
    self.mainCar.setLinearVelocity(self.mainCarVelocity)
    #self.drawTrajectory()

  def createImagesNN(self):
    input1 = [[self.peopleInfo, self.animalInfo, self.roadInfo]]
    input2 = [self.otherCarsInfo]
    input3 = [[self.roadInfo, self.treepoleInfo, self.riverInfo]]
    images1 = createImages(input1, 1)
    self.saveImages(images1, "Input 1")
    images2 = createImages(input2, 2)
    self.saveImages(images2, "Input 2")
    images3 = createImages(input3, 3)
    self.saveImages(images3, "Input 3")
    images4 = createImages([self.mainCarInfo[0]], 4)
    self.saveImages(images4, "Input 4")
    images5 = createImages([self.mainCarInfo[1]], 5)
    self.saveImages(images5, "Input 5")

  def saveImages(self, images, name):
    tipos = [['Meninos', 'Adultos', 'Idosos', 'Meninas', 'Adultas', 'Idosas', 'Animais', 'Faixa de pedestres', 'Status sinal'],['Outros carros'], ['Rodovia', 'Postes e Arvores', 'Rio'], 'Numero de passageiros Carro controlado', "Velocidade Carro controlado"]
    if len(images.shape)>3:
      for i in range(images.shape[0]):
        for j in range(images.shape[3]):
            pI = images[i,:,:,j]
            plt.figure()
            plt.subplot()
            title = name + " - " + tipos[self.auxImageCreator][j]
            plt.title(title)
            plt.ylim(0, 260)
            plt.yticks(np.arange(0, 260, 9.99))
            plt.xticks(np.arange(0, 80, 4.95))
            ax = plt.gca()
            ax.set_xticklabels(['-20' , '' , '' , '' , '' , '' , '' , '' , '0' , '' , '' , '' , '' , '' , '' , '' , '20' ])
            #new_labelsX = ['-20', '0', '', '', '', '0', '', '', ' 20']
            ax.set_yticklabels(['-30' , '' , '' , '' , '' , '' , '0' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '' , '', '' , '' , '' , '' , '' , '' , '95'  , ''])
            plt.imshow(pI, cmap = 'gray')
           
            #plt.colorbar()
            #ax.set_xticklabels(new_labelsX)
            #ax.set_yticklabels(new_labelsY)
            #plt.show()

            
            saveWhere = self.folderToSave + '/imagesNN/' + tipos[self.auxImageCreator][j] + '.pdf'
            plt.savefig(saveWhere, bbox_inches="tight")
    else:
      plt.figure()
      plt.subplot()
      title = name + " - " + tipos[self.auxImageCreator]
      plt.title(title)
      plt.imshow(images, cmap = 'gray')
      ax = plt.gca()
      plt.axes().get_yaxis().set_visible(False)
      if tipos[self.auxImageCreator] == 'Numero de passageiros Carro controlado':
        plt.xticks(np.arange(0, 80, 15.85))
        ax.set_xticklabels(['0', '1', '2', '3', '4', '5'])
      #plt.colorbar()
      saveWhere = self.folderToSave + '/imagesNN/' + tipos[self.auxImageCreator] + '.pdf'
      plt.savefig(saveWhere, bbox_inches="tight")
    self.auxImageCreator += 1

  def calcSteerAngles(self):
    X = np.arange(0.0, MAXSIMTIME + 5, TIMESTEP)
    #print [self.parameters[1]*sin(2*pi*self.parameters[2]*x + self.parameters[3]*pi) for x in X]
    self.steerAngles = iter([self.parameters[1]*sin(2*pi*self.parameters[2]*x + self.parameters[3]*pi) for x in X])

  def steerMainCar(self):
    a = next(self.steerAngles)
    self.mainCar.setSteerAngle(a)

  def changeCameraPosition(self):
    if not self.drawTrajectory:
      change = np.array(self.mainCar.bodyCar.getLinearVel())*TIMESTEP
      self.cameraPosition += change
      self.cameraFocalPoint += change
    else:
      self.cameraFocalPoint = (self.maxXPos/2, 0, 0)
      self.cameraPosition = (-self.maxXPos/2, self.maxXPos*2, 0)
    self.GetActiveCamera().SetPosition(self.cameraPosition)
    self.GetActiveCamera().SetFocalPoint(self.cameraFocalPoint)

  def changeMainCarVelocity(self):
    old = self.mainCarVelocity
    self.mainCarVelocity += self.parameters[0]*TIMESTEP
    if ((old >= 0 and self.mainCarVelocity < 0) or (old <= 0 and self.mainCarVelocity > 0)):
      self.mainCarVelocity = 0.0
    self.mainCar.setLinearVelocity(self.mainCarVelocity)
  
  def motionStart(self):
    for p in self.people:
      p.setLinearVelocity()
    for a in self.animal:
      a.setLinearVelocity()
    #for c,v in self.otherCars:
    #  c.setLinearVelocity(v)

  def inCrossPosition(self, pos):
    crossPos = self.road.crossPos
    if (crossPos > 0 and (crossPos - 1.5 <= pos <= crossPos + 1.5)):
      return True
    return False


  def execute(self, caller, event):
    self.motion()
    self.update()

  def iniciate(self):
    ode.InitODE()

  def getResult(self):
    if self.test:
      return self.collisions
    else:
      #return self.mainCar.getPosition()[0]
      out = self.insideRoad()
      return self.collisions, self.inRiver, out, self.distAuxCar#, self.mainCarPositions

  def insideRoad(self):
    maxPos = max(self.mainCarPositions, key = itemgetter(2))
    minPos = min(self.mainCarPositions, key = itemgetter(2))
    b, t = self.road.getSides()
    outTop, outBottom = 0, 0
    if not(t <= minPos[2] <= b):
      outTop = t - minPos[2]
    if not(t <= maxPos[2] <= b):
      outBottom = maxPos[2] - b 
    return max(outTop, outBottom)

  def close(self):
    ode.CloseODE()

  def getMinDistance(self):
    posMainCar = self.mainCar.getPosition()
    #print self.animal[0].getPosition(), np.linalg.norm(self.animal[0].bodyAnimal.getLinearVel())
    for p in self.people:
      posP = p.getPosition()
      diffCar = sqrt((posMainCar[0] - posP[0])**2 + (posMainCar[2] - posP[2])**2)
      if (self.road.crossPos > 0):
        sides = self.road.getSides()
        if (min(sides) <= posP[2] <= max(sides)):
          diffCross = sqrt((self.road.crossPos - posP[0])**2)  
        else:
          diffCross = 100
      else:
        diffCross = 1000
      if diffCar < self.distAuxCar[0]:
        self.distAuxCar = (diffCar, p.age, p.gender, self.mainCar.getLinearVelocity()) # distance, age, gender and velocity to calculate the risk of fatality
      if diffCross < self.distAuxCross:
        self.distAuxCross = diffCross
    if self.test:
      if not self.auxTest:
        self.collisions[13] = self.distAuxCar[0]
        self.collisions[14] = self.distAuxCross
    else:
      self.mainCarPositions.append(posMainCar)

  def checkStop(self):
    '''
    Check:
         if the mainCar has traveled at least a mininum distance after the last person 
         if its velocity is zero
         if the simulation time has passed
    '''
    posMainCar = self.mainCar.getPosition()
    velMainCar = self.mainCar.getLinearVelocity()

    if velMainCar < 0.01 and self.mySimulationTime > 1.0:
      self.stopCriteria = True
    else:
      countP, countA = 0, 0 # count how many people is already in a "safe zone"
      iP, iA = 0, 0
      for iP, p in enumerate(self.people):
        if (posMainCar[0] - p.getPosition()[0] > SAFEDISTANCETOSTOP):
          countP += 1
      if self.animal != []:
        for iA, a in enumerate(self.animal):
          if (posMainCar[0] - a.getPosition()[0] > SAFEDISTANCETOSTOP):
            countA += 1
      else:
        countA = 1
      if (countP == iP + 1 and countA == iA + 1):
        self.stopCriteria = True

    if self.mySimulationTime >= MAXSIMTIME:
      self.stopCriteria = True

    if self.folderToSave != None and self.drawTrajectory == False:
      saveImg = self.folderToSave + '/' + str(self.auxNumImg) + '.png'
      self.auxNumImg += 1
      #self.getScreenshot(saveImg)

    if self.visualization:
      if (self.mySimulationTime >= MAXSIMTIME or self.stopCriteria):
         self.end()
         if self.folderToSave != None and self.drawTrajectory == False:
          self.createGIF()
          self.saveAndDrawTrajectory()
          self.saveResult()
          self.saveParameters()


  def saveParameters(self):
    with open(self.folderToSave + '/parameters.txt', 'w') as parametersFile:
      json.dump(self.parameters, parametersFile)
  
  def saveAndDrawTrajectory(self):
    create = 'mkdir ' + self.folderToSave + '/trajectory'
    os.system(create)
    with open(self.folderToSave + '/trajectory/trajectory.txt', 'w') as trajFile:
      json.dump(self.mainCarPositions, trajFile)

  def saveResult(self):
    result = self.getResult()
    with open(self.folderToSave + '/result.txt', 'w') as resultFile:
      json.dump([result, self.mainCarInfo, self.roadInfo], resultFile)

  def createGIF(self):
    l1 = 'convert -delay 2 -loop 0 '+ self.folderToSave + '/{1..' + str(self.auxNumImg - 1) + '}.png ' + self.folderToSave + '/' + self.simName + '.gif'
    l2 = 'mv ' + self.folderToSave + '/trajectory/trajectory.png ' + self.folderToSave + 'trajectory/trajectory.png.keep'
    l3 = 'mv ' + self.folderToSave + '/imagesNN/situation.png ' + self.folderToSave + 'imagesNN/situation.png.keep'
    l4 = 'find ' + self.folderToSave + '/ -type f -iname \*.png -delete'
    l5 = 'mv ' + self.folderToSave + '/trajectory/trajectory.png.keep ' + self.folderToSave + 'trajectory/trajectory.png'
    l6 = 'mv ' + self.folderToSave + '/imagesNN/situation.png.keep ' + self.folderToSave + 'imagesNN/situation.png'
    with open('generateGif.txt', 'a') as gifFile:
      gifFile.write(l1)
      gifFile.write('\n')
      gifFile.write(l2)
      gifFile.write('\n')
      gifFile.write(l3)
      gifFile.write('\n')
      gifFile.write(l4)
      gifFile.write('\n')
      gifFile.write(l5)
      gifFile.write('\n')
      gifFile.write(l6)
      gifFile.write('\n')

  def reduceVelocity(self):
    mcPos = self.mainCar.getPosition()
    for i, car in enumerate(self.otherCars):
      c, v = car
      cPos = c.getPosition()
      if (abs(mcPos[2] - cPos[2]) < 1):
        if (abs(mcPos[0] - cPos[0]) < 15):
          if (mcPos[0] - cPos[0] > 0):
            if (self.mainCarVelocity < v):
              c.setLinearVelocity(self.mainCarVelocity)
              self.otherCars[i] = (c, self.mainCarVelocity)
          else:
            if (self.mainCarVelocity > v):
              self.mainCar.setLinearVelocity(v)
              self.mainCarVelocity = v
    for i, car1 in enumerate(self.otherCars):
      c, v = car1
      cPos = c.getPosition()
      for j, car2 in enumerate(self.otherCars):
        c2, v2 = car2
        c2Pos = c2.getPosition()
        if (abs(c2Pos[2] - cPos[2]) < 1):
          if (abs(c2Pos[0] - cPos[0]) < 15):
            if (cPos[0] - c2Pos[0] > 0):
              if (v < v2):
                c2.setLinearVelocity(v)
                self.otherCars[j] = (c2, v)
            else:
              if (v > v2):
                c.setLinearVelocity(v2)
                self.otherCars[i] = (c, v2)

  def trajectory(self):
    with open(self.folderToSave + '/trajectory/trajectory.txt') as trajFile:
      trajectory = json.load(trajFile)
    p = []
    enabled = False
    self.maxXPos = 0
    for i in range(len(trajectory) - 1):
      if abs(trajectory[i][0]) < 1:
        enabled = True
      if enabled:
        if trajectory[i][0] > self.maxXPos:
          self.maxXPos = trajectory[i][0]
        p.append((trajectory[i][0], BASEHEIGHT + 1, trajectory[i][2], trajectory[i+1][0], BASEHEIGHT + 0.1, trajectory[i+1][2], 0))
    self.drawLines(p, lineWidth = 3, lineColor = (1,0.5,0))

  def motion(self):
    if self.visualization:
      self.changeCameraPosition()
      pass

    self.getMinDistance()

    #reduce velocity cars in the same lane
    if self.auxReduceVelocity:
      self.reduceVelocity()
      
    if (self.mainCar.inPosition()):
      if self.visualization:
        #pass
        if self.folderToSave != None and self.drawTrajectory == False:
          self.getScreenshot(self.folderToSave+'/imagesNN/situation.png')
        if self.drawTrajectory:
          self.changeCameraPosition()
          self.getScreenshot(self.folderToSave+'/trajectory/trajectory.png')
      self.auxReduceVelocity = False  #enable vehicle collision
      self.startBrakeandSteer = self.mySimulationTime + self.parameters[4]

    if self.startBrakeandSteer <= self.mySimulationTime and not self.test and self.auxBrake:
      self.mainCar.brake(self.parameters[0])
      self.enableSteer = True
      self.auxBrake = False

    if self.enableSteer:
      self.steerMainCar()

    self.checkStop()
    
    n = 2
    for _ in range(n):
        # Detect collisions and create contact joints
        self.space.collide((self.world, self.contactgroup), self.near_callback)
        # Simulation step
        self.world.step(TIMESTEP/n)
        # Remove all contact joints
        self.contactgroup.empty()
    self.mySimulationTime += TIMESTEP
    #print "#"*70
    #print self.mySimulationTime, self.mainCar.getLinearVelocity()
    #print self.mainCar.getLinearVelocity(), self.mainCar.getPosition(), self.mySimulationTime

  def simulate(self):
    if self.visualization:
      self.start()
    else:
      while not self.stopCriteria: 
       self.motion()

  def near_callback(self, args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.
    """
    body1 = geom1.getBody()
    body2 = geom2.getBody()

    # Contacts in the same group are ignored
    # e.g. foot and lower leg
    for group in allGroups:
        if body1 in group and body2 in group:
          return
    
    # Check if the objects do collide    
    contacts = ode.collide(geom1, geom2)
    try:
      g1Name = geom1.__getattribute__('name')
      g2Name = geom2.__getattribute__('name')
    except:
      print self.simName
      print geom1, geom2


    if self.test:
      if (not self.mainCar.inPosition() and self.auxTest):
        if g1Name != g2Name:
          if g1Name not in ['Road', 'Base', 'Floor'] and g2Name not in ['Road', 'Base', 'Floor']:
            self.collisions = True
            self.stopCriteria = True
      else:
        #print "Colisao entre: ", g1Name, " e ", g2Name
        self.auxTest = False
        if g1Name == "MainCar" or g2Name == "MainCar":
          if "Person" in g1Name:
            if self.inCrossPosition(geom1.getPosition()[0]):
              "adicionar pessoa nas laterais"
              self.collisions[0] = 1
              if (self.roadInfo[4]): #statusSemaphore
                 self.collisions[2] = 1
            else:
              self.collisions[1] = 1
            if "MaleKid" in g1Name:
              self.collisions[3] = 1
            elif "MaleMiddle" in g1Name:
              self.collisions[4] = 1
            elif "MaleOld" in g1Name:
              self.collisions[5] = 1
            elif "FemaleKid" in g1Name:
              self.collisions[6] = 1
            elif "FemaleMiddle" in g1Name:
              self.collisions[7] = 1
            elif "FemaleOld" in g1Name:
              self.collisions[8] = 1
          elif"Person" in g2Name:
            if self.inCrossPosition(geom2.getPosition()[0]):
              self.collisions[0] = 1
              if (self.roadInfo[4]): #statusSemaphore
                 self.collisions[2] = 1
            else:
              self.collisions[1] = 1
            if "MaleKid" in g2Name:
              self.collisions[3] = 1
            elif "MaleMiddle" in g2Name:
              self.collisions[4] = 1
            elif "MaleOld" in g2Name:
              self.collisions[5] = 1
            elif "FemaleKid" in g2Name:
              self.collisions[6] = 1
            elif "FemaleMiddle" in g2Name:
              self.collisions[7] = 1
            elif "FemaleOld" in g2Name:
              self.collisions[8] = 1
          elif "Animal" in g1Name or "Animal" in g2Name:
            self.collisions[9] = 1
          elif "OtherCar" in g1Name or "OtherCar" in g2Name:
            self.collisions[10] = 1
          elif "Pole" in g1Name or "Pole" in g2Name:
            self.collisions[11] = 1
          elif "Road" in g1Name or "Road" in g2Name or "Base" in g1Name or "Base" in g2Name:
            self.collisions[12] = 1

        #self.collisions = False
        #self.stopCriteria = True
    else:
      #if ("Car" in g1Name or "Car" in g2Name) and ("Person" in g1Name or "Person" in g2Name):
        #print g1Name, g2Name
      if ((g1Name == "River") or (g2Name == "River")):
        otherName = g1Name if g2Name == "River" else g2Name
        if "Wheel" in otherName:
          otherName = otherName.replace("Wheel", "")
        if otherName in map(itemgetter('geomName'), self.collisions) or otherName == "MainCar":
          if otherName not in self.inRiver:
            self.inRiver.append(otherName)
      else:
        #if "Car" in g1Name and "Car" in g2Name:
          #print g1Name, g2Name  

        if ((g1Name == "MainCar" or g2Name == "MainCar") and ('Wheel' not in g1Name and 'Wheel' not in g2Name) and ('Floor' not in g1Name and 'Floor' not in g2Name)):          
          if len(contacts) != 0:
            #mcV, mcP, cP, outra Pos (ver se foi so de raspao o atropelamento)
            for c in contacts:
              pos, _, normal, geom1, geom2 = c.getContactGeomParams()
              if g1Name == "MainCar":
                posMainCar = geom1.getPosition()
                geomName = g2Name
                geomPos = geom2.getPosition()
              else:
                posMainCar = geom2.getPosition()
                geomName = g1Name
                geomPos = geom1.getPosition()
              index = map(itemgetter('geomName'), self.collisions).index(geomName) if geomName in map(itemgetter('geomName'), self.collisions) else None

              if index == None or self.collisions[index]['normal'] < normal:
                if index != None:
                  del self.collisions[index]

                contactDict = {"pos"      : pos, \
                             "posMainCar" : posMainCar, \
                             "geomName"   : geomName, \
                             "geomPos"    : geomPos, \
                             "mainCarVel" : self.mainCar.getLinearVelocity(), \
                             "normal"     : normal,
                             "geomVel"    : np.linalg.norm(geom2.getBody().getLinearVel()) if "OtherCar" in geomName else 0,
                             "angle"      : acos(geom1.getRotation()[0]) - acos(geom2.getRotation()[0])}
                self.collisions.append(contactDict)

    # Create contact joints
    self.world, self.contactgroup = args

    for c in contacts:
        c.setBounce(0.2)
        if (("Car" in g1Name and "Person" in g2Name) or ("Car" in g2Name and "Person" in g1Name) or ("Car" in g1Name and "Animal" in g2Name) or ("Car" in g2Name and "Animal" in g1Name)):
          c.setMode(26)
          c.setBounce(0.2)
          c.setSoftERP(0.001)
          c.setSoftCFM(0.005) 
        c.setMu(5000)
        j = ode.ContactJoint(self.world, self.contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())