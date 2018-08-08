import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin, sqrt
import numpy as np
from objects import *
from constants import *

class Sim(ode_viz.ODE_Visualization):
  def __init__(self, mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo, animalInfo, name, test, visualization):
    self.iniciate()
    self.createWorld()
    self.mainCarInfo = mainCarInfo        # (numPassengers, velocity, inicialSteerAngle, inicialDistance)
    self.mainCarVelocity = self.mainCarInfo[1]
    self.roadInfo = roadInfo              # (nLanes, direction, position mainCar, crosswalk position, status semaphore)
    self.peopleInfo = peopleInfo          # [(position, velocity, num)], position = x, z, theta
    self.otherCarsInfo = otherCarsInfo    # [(position, direction, velocity, inicialDistance, num)], position = x, 0, z
    self.treepoleInfo = treepoleInfo      # [(x, z, tree, num)], z is 0 or 1 corresponding the side of the road, tree is 0 or 1: 0 - pole, 1 - tree
    self.animalInfo = animalInfo          # [(position, velocity, num)]
    self.parameters = parameters          # parameters from the genetic algorithm
    self.calcSteerAngles()
    if visualization:
      ode_viz.ODE_Visualization.__init__(self, self.world, [self.space], TIMESTEP)
      self.visualization = self
      self.space = self.space[0]  
    else:
      self.visualization = False
    self.otherCars = []
    self.people = []
    self.animal = []
    self.createBase()
    self.createObjects()
    self.cameraFocalPoint = np.array(self.mainCar.getPosition()) + (10, 0, 0) #- (ROADLENGTH/2 - 100.0, 0, 0)
    self.cameraPosition = np.array(self.cameraFocalPoint) - (30, -40, 0)    
    if self.visualization:
      self.changeCameraPosition()
      self.SetSize(800, 600)
      title = "Simulation " + name
      self.SetWindowName(title)
      self.SetBackground(50./255, 153./255, 204./255)
    self.aux = 0
    self.simName = name
    self.test = test
    self.stopCriteria = False
    self.fitness = None
    self.collisions = [0, 0, 0, 0, 0, 0, 1000, 1000]
    self.enableSteer = False
    self.auxTest = True
    self.mySimulationTime = 0
    self.distAuxCar = 1000
    self.distAuxCross = 1000

    self.contactgroup = ode.JointGroup()

  def createBase(self):
    #create a plane geom which prevent the objects from falling forever
    self.floor = ode.GeomPlane(self.space, (0, 1, 0), 0)
    if self.visualization:
      self.addGeom(self.floor)
    self.floor.__setattr__('name','Floor')
    #create a base 
    self.geomBase = ode.GeomBox(self.space, (BASELENGTH, BASEHEIGHT, BASEWIDTH))
    self.geomBase.setPosition((BASELENGTH/2 - 500.0, BASEHEIGHT/2, 0.0))
    fxJoint = ode.FixedJoint(self.world)
    fxJoint.attach(self.geomBase.getBody(), ode.environment)
    fxJoint.setFixed()
    if self.visualization:
      self.addGeom(self.geomBase)
      self.GetObject(self.geomBase).SetTexture('Images/floor.jpeg')
    self.geomBase.__setattr__('name','Base')

  def createWorld(self):
    #create world
    self.world = ode.World()
    self.world.setGravity(GRAVITY)
    self.world.setERP(0.8)
    self.world.setCFM(1E-5)
    #create Space
    self.space = ode.Space()
      

  def createObjects(self):
    self.road = Road(self.world, self.space, self.visualization, self.roadInfo[0], self.roadInfo[1], self.roadInfo[2], self.roadInfo[3], self.roadInfo[4])
    self.mainCar = Car(self.world, self.space, self.visualization, self.mainCarInfo[3], passengers = self.mainCarInfo[0]) 
    sideTop, sideBottom = self.road.getSides()
    if (self.treepoleInfo != None):
       for tp in self.treepoleInfo:
          if tp[1] == 0:
             s = sideTop + 1
          else:
             s = sideBottom - 1
          TreePole(self.world, self.space, self.visualization, (tp[0], 0, s), tp[2], tp[3])
    if (self.peopleInfo != None):
       for p in self.peopleInfo:
          self.people.append(Person(self.world, self.space, self.visualization, p[0], p[1], p[2], p[3]))
       
    if (self.animalInfo != None):
        for a in self.animalInfo:
          self.animal.append(Animal(self.world, self.space, self.visualization, a[0], a[1], a[2], a[3]))
        for persona in self.animal:
           print "setando vec"
           persona.setLinearVelocity()
    if (self.otherCarsInfo != None):
       for c in self.otherCarsInfo:
          car = Car(self.world, self.space, self.visualization, c[3], mainCar = False, position = c[0], direction = c[1], num = c[5])
          car.setLinearVelocity(c[2])
          car.setSteerAngle(0.0)
          self.otherCars.append((car, c[2]))
    self.mainCar.setSteerAngle(self.mainCarInfo[2])
    self.mainCar.setLinearVelocity(self.mainCarVelocity)

  def calcSteerAngles(self):
    X = np.arange(0.0, MAXSIMTIME + 5, TIMESTEP)
    self.steerAngles = iter([self.parameters[1]*sin(2*pi*self.parameters[2]*x + self.parameters[3]) for x in X])

  def changeCameraPosition(self):
    change = np.array(self.mainCar.bodyCar.getLinearVel())*TIMESTEP
    self.cameraPosition += change
    self.cameraFocalPoint += change
    self.GetActiveCamera().SetPosition(self.cameraPosition)
    self.GetActiveCamera().SetFocalPoint(self.cameraFocalPoint)

  def changeMainCarVelocity(self):
    old = self.mainCarVelocity
    self.mainCarVelocity += self.parameters[0]*TIMESTEP
    if ((old >= 0 and self.mainCarVelocity < 0) or (old <= 0 and self.mainCarVelocity > 0)):
      self.mainCarVelocity = 0.0
    self.mainCar.setLinearVelocity(self.mainCarVelocity)

  def steerMainCar(self):
    a = next(self.steerAngles)
    self.mainCar.setSteerAngle(a)

  def motionStart(self):
    for p in self.people:
      print "ABACATE"
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
    return self.animal[0].bodyAnimal.getPosition()[0], self.mySimulationTime
    return self.collisions

  def close(self):
    ode.CloseODE()

  def motion(self):
    if self.visualization:
      self.changeCameraPosition()

    self.aux += 1
    if (self.mainCar.inPosition()):
      #self.motionStart()
      #self.mainCar.brake([self.parameters[0], self.parameters[0]])
      self.enableSteer = True
    if self.enableSteer:
      self.steerMainCar()

    if self.test and not self.auxTest:
      posMainCar = self.mainCar.getPosition()
      
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
        if diffCar < self.distAuxCar:
          self.distAuxCar = diffCar
          self.collisions[6] = diffCar
        if diffCross < self.distAuxCross:
          self.distAuxCross = diffCross
          self.collisions[7] = diffCross


    #self.changeMainCarVelocity()
    #self.steerMainCar()
    #print self.mainCar.bodyFWL.getLinearVel()
    #print self.people[0].body.getLinearVel()[0], self.peopleInfo[0][2]
    if (self.animal[0].bodyAnimal.getLinearVel()[0] > self.animalInfo[0][1] - 0.05):
      self.stopCriteria = True
    #if (self.mainCar.getLinearVelocity() > self.mainCarVelocity - 0.05):
    #  self.stopCriteria = True
      #print self.aux*TIMESTEP, self.mainCar.getLinearVelocity(), self.mainCar.flMotorRoll.getParam(ode.ParamVel)
    if self.visualization:
      if (self.mySimulationTime >= MAXSIMTIME or self.stopCriteria):
         self.end()
    if self.mySimulationTime >= MAXSIMTIME:
      self.stopCriteria = True
    n = 2
    for _ in range(n):
        # Detect collisions and create contact joints
        self.space.collide((self.world, self.contactgroup), self.near_callback)
        # Simulation step
        self.world.step(TIMESTEP/n)
        # Remove all contact joints
        self.contactgroup.empty()
    self.mySimulationTime += TIMESTEP

  def simulate(self):
    if self.visualization:
      self.start()
    else:
      while not self.stopCriteria:
        #print "estou no while"
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

    g1Name = geom1.__getattribute__('name')
    g2Name = geom2.__getattribute__('name')

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
            else:
              self.collisions[1] = 1
          elif"Person" in g2Name:
            if self.inCrossPosition(geom2.getPosition()[0]):
              self.collisions[0] = 1
            else:
              self.collisions[1] = 1
          elif "Animal" in g1Name or "Animal" in g2Name:
            self.collisions[2] = 1
          elif "OtherCar" in g1Name or "OtherCar" in g2Name:
            self.collisions[3] = 1
          elif "Pole" in g1Name or "Pole" in g2Name:
            self.collisions[4] = 1
          elif "Road" in g1Name or "Road" in g2Name or "Base" in g1Name or "Base" in g2Name:
            self.collisions[5] = 1

        #self.collisions = False
        #self.stopCriteria = True
    else:
      if g1Name == "MainCar" or g2Name == "MainCar":
        if len(contacts) != 0:
          self.collisions.append([g1Name, g2Name, contacts])

    # Create contact joints
    self.world, self.contactgroup = args

    for c in contacts:
        #mudar bounce e mu conforme colisao
        c.setBounce(0.2)
        if (("Car" in g1Name and "Person" in g2Name) or ("Car" in g2Name and "Person" in g1Name) or ("Car" in g1Name and "Animal" in g2Name) or ("Car" in g2Name and "Animal" in g1Name)):
          c.setSoftCFM(1)
          c.setSoftERP(1)
          #abaixar carro?
        c.setMu(5000)
        j = ode.ContactJoint(self.world, self.contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

