import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin
import numpy as np
from objects import *
from constants import *

class Sim(ode_viz.ODE_Visualization):
  def __init__(self, mainCar, road, people, otherCars = None, trees = None, poles = None):
    self.createWorld()
    ode_viz.ODE_Visualization.__init__(self, self.world, [self.space], TIMESTEP)
    self.createObjects()
    self.cameraFocalPoint = np.array(self.road.body.getPosition()) + (10, 0, 0)
    self.cameraPosition = np.array(self.cameraFocalPoint) - (30, -40, 0)    
    self.changeCameraPosition()
    self.SetSize(800, 600)
    self.SetWindowName("Simulation")
    self.SetBackground(50./255, 153./255, 204./255)
    self.addGeom(self.floor)
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

  def createObjects(self):
    self.road = Road(self.world, self.space, self, 4, 1, 2)
    self.mainCar = Car(self.world, self.space, self, self.road)
    sideTop, sideBottom = self.road.getSides()
    self.tree = TreePole(self.world, self.space, self, (10, 0, sideTop + 0.4))
    self.pole = TreePole(self.world, self.space, self, (10, 0, sideBottom - 0.4), False)
    #self.person = Person(self.world, self.space, self, (5, 0, sideBottom + 0.5), (15,0,15), self.road)
    self.othercar = Car(self.world, self.space, self, self.road, mainCar = False, position = (40, 0 , -3), direction = -1)
    self.othercar.setLinearVelocity((30,0,0))

  def changeCameraPosition(self):
    change = np.array(self.mainCar.bodyCar.getLinearVel())*TIMESTEP
    self.cameraPosition += change
    self.cameraFocalPoint += change
    self.GetActiveCamera().SetPosition(self.cameraPosition)
    self.GetActiveCamera().SetFocalPoint(self.cameraFocalPoint)

  def execute(self, caller, event):
    self.motion()
    self.update()

  def motion(self):
    #self.changeCameraPosition()
    #print self.person.body.getLinearVel()
    self.mainCar.addTorque(40)
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

        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(self.world, self.contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

sim = Sim(0, 0, 0)
sim.start()
