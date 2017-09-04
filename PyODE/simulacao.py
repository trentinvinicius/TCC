import ode, xode.parser
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin
import numpy as np
from objects import *

#Definitions
fps = 30.0
dt = 1.0/fps

global allGroups

# pesquisar maxima taxa de steering
# usar velocidade angular para girar as rodas - definir limites

#  Disabling bodies is an effective way to save computation time when it is known that the bodies are motionless or otherwise irrelevant to the simulation.
''''um dos algoritmos mais conhecidos usados para o
controle de carros eh atraves do ajuste da trajetoria do
veiculo baseada em uma trajetoria virtual. Esta
trajetoria virtual eh denominada de way-point, ou seja, uma sequencia de pontos que definem o caminho que
deveria ser seguido (aproximadamente). Encontramos
na literatura sobre jogos (e de robotica) uma extensa
bibliografia descrevendo tecnicas baseadas em waypoints,
a exemplo das citadas nos livros da serie A.I.
game programming wisdom [Rabin 2001, 2002]. '''

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

#create World
world = ode.World()
world.setGravity((0, -9.81, 0))
world.setERP(0.8)
world.setCFM(1E-5)

#create Space
space = ode.Space()

bodies = []
geoms = []

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0, 1, 0), -4)

def idlefunc():
    n = 2
    ang = c.flJoint.getAngle2Rate()
    ang2 = c.frJoint.getAngle2Rate()
    print ang, ang2
    


    for _ in range(n):
        # Detect collisions and create contact joints
        c.addTorque(10)

        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()

class my_sim(ode_viz.ODE_Visualization):
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

viz = my_sim(world, [space], dt)
#car()
c = Car(world,[space],viz)
c.addTorque(100.0)
#c.setLinearVelocity((0.1,0,0))
#p = Person(world, [space], viz, (5, 0, 3), (0, 0, 5))
global allGroups
'''groups = []
        
for group in allGroups:
  groups = groups + group
allGroups = groups'''
viz.start()
