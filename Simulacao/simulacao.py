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

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0, 1, 0), -4)
i = 0
j = 0
se = 0


def idlefunc():    
    global i, c2, j, se
    
    c2.addTorque(40)
    #print c2.getSteerAngle() 

    pos = np.array(c2.bodyCar.getPosition())
    #print pos
    #viz.GetActiveCamera().SetFocalPoint(pos)
    
    if i > 1000:  
      ang = -pi/6
    else:
      ang = pi/6

    pos[1] += 20
    pos[0] -= 20*cos(ang)
    pos[2] -= 20*sin(ang)

    #c2.setSteerAngle(ang)
    i += 1
    #viz.GetActiveCamera().SetPosition(pos)
    
    #c2.addTorque(10)
    '''
    c = c2.bodyFWL.getRotation()
    #print c 
    #c2.setLinearVelocity((0.5,0,0))
    c2.bodyRWL.setAngularVel((1.5, 0.0, 0.0))
    c2.bodyRWR.setAngularVel((1.5, 0.0, 0.0))
    i += 1
    if (i%10 == 0):
      ang = (j*pi/180)
      if (se == 0):
        if j < 30:
          j += 1
        else:
          se = 1
          j -= 1
      else:
        if j > -30:
          j -= 1
        else:
          se = 0
          j += 1
      c2.steer(ang)
      print ang*180/pi
    '''
    n = 2
    for _ in range(n):
        # Detect collisions and create contact joints
        

        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()


class my_sim(ode_viz.ODE_Visualization):
   def __init__(self, world, space, dt):
      ode_viz.ODE_Visualization.__init__(self, world, space, dt)
      #self.space = space
      self.GetActiveCamera().SetPosition(0.28, 28.878, 50.654)
      self.GetActiveCamera().SetFocalPoint(-0.1105, 2.8448, -0.4285)
      self.GetActiveCamera().SetViewUp(0.002656, 0.9038, -0.4278)
      self.SetSize(800,600)
      self.SetWindowName("Simulacao")
      self.SetBackground(50./255,153./255,204./255)
      #road = road = Road(world, space, self, 2)
      #self.c3 = Car(world, space, self, road)
   def execute(self, caller, event):
      idlefunc()
      self.update()
   def teste(self, a):
      return self.GetActor(a)
   
viz = my_sim(world, [space], dt)
#car()
#c = Car(world,[space],viz, mainCar = False, direction = 1, position = (10, 0, 0))
road = Road(world, [space], viz, 2)
c2 = Car(world, [space], viz, road)
#c2.steer(pi/6)
#c2.bodyCar.
#c.setLinearVelocity((1,0,0))
#c2.setLinearVelocity((0.5,0,0))
#c2.steer(100.0)
#c.addTorque(-100.0)
#c2.addTorque(1000.0)
#c.setLinearVelocity((0.1,0,0))
#p = Person(world, [space], viz, (5, 0, 3), (0, 0, 5))
global allGroups
'''groups = []
        
for group in allGroups:
  groups = groups + group
allGroups = groups'''



viz.start()
