import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin
import numpy as np
from objects import *
from constants import *

global mainCar
global viz
class Sim(object):
	def __init__(self):
		global viz
		self.createWorld()
		self.viz = Visualization(self.world, [self.space], TIMESTEP)
		viz = self.viz
		self.createObjects()

	def createWorld(self):
		#create world
		self.world = ode.World()
		self.world.setGravity(GRAVITY)
		self.world.setERP(0.8)
		self.world.setCFM(1E-5)
		#create Space
		self.space = ode.Space()
		# Create a plane geom which prevent the objects from falling forever
		self.floor = ode.GeomPlane(self.space, (0, 1, 0), -4)

	def createObjects(self):
		self.road = Road(self.world, [self.space], self.viz, 2)
		global mainCar
		mainCar = Car(self.world, [self.space], self.viz, self.road)

	def run(self):
		self.viz.start()

class Visualization(ode_viz.ODE_Visualization):
   def __init__(self, world, space, dt):
      ode_viz.ODE_Visualization.__init__(self, world, space, dt)
      self.GetActiveCamera().SetPosition(0.28, 28.878, 50.654)
      self.GetActiveCamera().SetFocalPoint(-0.1105, 2.8448, -0.4285)
      self.GetActiveCamera().SetViewUp(0.002656, 0.9038, -0.4278)
      self.SetSize(800,600)
      self.SetWindowName("Simulacao")
      self.SetBackground(50./255,153./255,204./255)
   def execute(self, caller, event):
      idlefunc()
      self.update()

contactgroup = ode.JointGroup()

def near_callback(args, geom1, geom2):
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
    world,contactgroup = args
    for c in contacts:

        c.setBounce(0.2)
        c.setMu(5000)
        j = ode.ContactJoint(world, contactgroup, c)
        j.attach(geom1.getBody(), geom2.getBody())

i = 0
j = 0
se = 0


def idlefunc():    
    global i, mainCar, j, se
    
    mainCar.addTorque(40)
    print mainCar.getSteerAngle() 

    pos = np.array(mainCar.bodyCar.getPosition())
    print pos
    viz.GetActiveCamera().SetFocalPoint(pos)
    
    if i > 1000:
      ang = -pi/6
    else:
      ang = pi/6

    pos[1] += 20
    pos[0] -= 20*cos(ang)
    pos[2] -= 20*sin(ang)

    #mainCar.setSteerAngle(ang)
    i += 1
    viz.GetActiveCamera().SetPosition(pos)
    n = 2
    for _ in range(n):
        # Detect collisions and create contact joints
        

        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()


   
sim = Sim()
sim.run()