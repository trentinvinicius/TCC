import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin
import numpy as np
from objects import *
from constants import *

class Sim(ode_viz.ODE_Visualization):
  def __init__(self, mainCarInfo, roadInfo, peopleInfo, parameters, otherCarsInfo, treepoleInfo, name, test):
    self.iniciate()
    self.createWorld()
    self.mainCarInfo = mainCarInfo        # (numPassengers, velocity, inicialSteerAngle, inicialDistance)
    self.mainCarVelocity = self.mainCarInfo[1]
    self.roadInfo = roadInfo              # (nLanes, direction, position mainCar)
    self.peopleInfo = peopleInfo          # [(position, velocity)], position = x, z, theta
    self.otherCarsInfo = otherCarsInfo    # [(position, direction, velocity, inicialDistance)], position = x, 0, z
    self.treepoleInfo = treepoleInfo      # [(x, z, tree)], z is 0 or 1 corresponding the side of the road, tree is 0 or 1: 0 - pole, 1 - tree
    self.parameters = parameters          # parameters from the genetic algorithm
    self.calcSteerAngles()
    ode_viz.ODE_Visualization.__init__(self, self.world, [self.space], TIMESTEP)
    self.otherCars = []
    self.people = []
    self.createObjects()
    self.cameraFocalPoint = np.array(self.mainCar.getPosition()) + (10, 0, 0) #- (ROADLENGTH/2 - 100.0, 0, 0)
    self.cameraPosition = np.array(self.cameraFocalPoint) - (30, -40, 0)    
    self.changeCameraPosition()
    self.SetSize(800, 600)
    title = "Simulation " + name
    self.SetWindowName(title)
    self.SetBackground(50./255, 153./255, 204./255)
    self.addGeom(self.floor)
    self.addGeom(self.base)
    self.GetObject(self.base).SetTexture('Images/floor.jpeg')
    self.aux = 0
    self.simName = name

    self.contactgroup = ode.JointGroup()

  def createWorld(self):
		#create world
    self.world = ode.World()
    self.world.setGravity(GRAVITY)
    self.world.setERP(0.8)
    self.world.setCFM(1E-5)
		#create Space
    self.space = ode.Space()
		# Create a plane geom which prevent the objects from falling forever
    self.floor = ode.GeomPlane(self.space, (0, 1, 0), 0)
    self.base = ode.Body(self.world)
    self.bMass = ode.Mass()
    self.bMass.setBox(BASEDENSITY, BASELENGTH, BASEHEIGHT, BASEWIDTH)
    self.base.setMass(self.bMass)
    self.geomBase = ode.GeomBox(self.space, (BASELENGTH, BASEHEIGHT, BASEWIDTH))
    self.geomBase.setBody(self.base)
    self.geomBase.setPosition((BASELENGTH/2 - 100.0, BASEHEIGHT/2, 0.0))
    self.base.disable()

  def createObjects(self):
    self.road = Road(self.world, self.space, self, self.roadInfo[0], self.roadInfo[1], self.roadInfo[2])
    self.mainCar = Car(self.world, self.space, self, self.mainCarInfo[3], passengers = self.mainCarInfo[0]) 
    sideTop, sideBottom = self.road.getSides()
    if (self.treepoleInfo != None):
       for tp in self.treepoleInfo:
          if tp[1] == 0:
             s = sideTop + 1
          else:
             s = sideBottom - 1
          TreePole(self.world, self.space, self, (tp[0], 0, s), tp[2], self.base)
    if (self.peopleInfo != None):
       for p in self.peopleInfo:
          self.people.append(Person(self.world, self.space, self, p[0], p[1]))

    if (self.otherCarsInfo != None):
       for c in self.otherCarsInfo:
          car = Car(self.world, self.space, self, c[3], mainCar = False, position = c[0], direction = c[1])
          #car.setLinearVelocity(c[2])
          car.setSteerAngle(0.0)
          self.otherCars.append((car, c[2]))
    self.mainCar.setSteerAngle(self.mainCarInfo[2])
    self.mainCar.setLinearVelocity(self.mainCarVelocity)

  def calcSteerAngles(self):
    X = np.arange(0.0, MAXSIMTIME, TIMESTEP)
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
    print a
    self.mainCar.setSteerAngle(a)

  def motionStart(self):
    for p in self.people:
      p.setLinearVelocity()
    for c,v in self.otherCars:
      c.setLinearVelocity(v)

  def execute(self, caller, event):
    self.motion()
    self.update()

  def iniciate(self):
    ode.InitODE()

  def getFitness(self):
    return self.simulationTime, self.mainCar.getPosition()[0]

  def close(self):
    ode.CloseODE()

  def motion(self):
    #print self.simName, self.mainCar.getPosition()
    self.changeCameraPosition()
    self.aux += 1
    if (self.mainCar.inPosition()):
      self.motionStart()
    #print self.mainCar.flMotorRoll.getFeedback()
    #self.changeMainCarVelocity()
    #self.steerMainCar()
    #print self.mainCar.bodyFWL.getLinearVel()
    if (self.mainCar.getLinearVelocity() > self.mainCarVelocity - 0.05):
      pass
      #self.end()
      #print self.aux*TIMESTEP, self.mainCar.getLinearVelocity(), self.mainCar.flMotorRoll.getParam(ode.ParamVel)
    if (self.simulationTime >= MAXSIMTIME):
       #pass
       #self.mainCar.brake()
       self.end()
    n = 2
    for _ in range(n):
        # Detect collisions and create contact joints
        self.space[0].collide((self.world, self.contactgroup), self.near_callback)
        # Simulation step
        self.world.step(TIMESTEP/n)
        # Remove all contact joints
        self.contactgroup.empty()

  def near_callback(self, args, geom1, geom2):
    """Callback function for the collide() method.

    This function checks if the given geoms do collide and
    creates contact joints if they do.
    """
    body1 = geom1.getBody()
    body2 = geom2.getBody()
    print type(body1)
    # Contacts in the same group are ignored
    # e.g. foot and lower leg
    for group in allGroups:
        if body1 in group and body2 in group:
            return

    # Check if the objects do collide
    contacts = ode.collide(geom1, geom2)

    # Create contact joints
    self.world, self.contactgroup = args

    for c in contacts:
        #mudar bounce e mu conforme colisao
        #fixar geometrias
        c.setBounce(0.2)
        c.setMu(5000)
        if geom1 == self.geomBase and geom2 == self.floor:
          c.setBounce(0.0)
          c.setMu(500000)
        j = ode.ContactJoint(self.world, self.contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())
        #pesquisar juntas entre geometrias
        #anexar geometrias no universo

