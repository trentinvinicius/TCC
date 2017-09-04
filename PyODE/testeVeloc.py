import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin
import numpy as np

# Create a world object
world = ode.World()
world.setGravity((0, -9.81, 0))
world.setERP(0.8)
world.setCFM(1E-5)

# Create a space object
space = ode.Space()

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0, 1, 0), 0)
floor.enable()


body = ode.Body(world)
M = ode.Mass()
M.setBox(100, 1, 2, 3)
#M.mass = 1.0

Tree = ode.Mass()
Tree.setCylinder(100, 3, 3, 10)

Treebody = ode.Body(world)

Treebody.setMass(Tree)
body.setMass(M)

#body.addForce((0,10,0))




body.setPosition( (0,0,0) )
#body.addForce( (0,200,0) )
geomTree = ode.GeomCylinder(space, 3, 10)
geomTree.setBody(Treebody)
geom = ode.GeomBox(space, lengths = (1, 2, 3))
geom.setBody(body)
ang = pi/2
rotation = np.array([[1, 0, 0],[0, cos(ang), -sin(ang)],[0, sin(ang), cos(ang)]])
print rotation.reshape(1,9)[0]
geomTree.setRotation((rotation.reshape(1,9)[0]))
body.setPosition((0,1,0))
body.setLinearVel((0.1,0,0))

Treebody.setPosition((10,5,30))
fps = 10
dt = 0.1





class my_sim(ode_viz.ODE_Visualization):
   def __init__(self, world, space, dt):
      ode_viz.ODE_Visualization.__init__(self, world, space, dt)
      self.GetActiveCamera().SetPosition(0.028, 11.878, 18.654)
      self.GetActiveCamera().SetFocalPoint(-0.1105, 2.8448, -0.4285)
      self.GetActiveCamera().SetViewUp(0.002656, 0.9038, -0.4278)
   def execute(self, caller, event):
      self.update()
      world.step(dt)
      u,v,w = body.getPosition()
      print "Pos: ", u,v,w
viz = my_sim(world, [space], dt)
viz.GetProperty(body).SetColor(0,255,0)
viz.addGeom(geom)
viz.addGeom(geomTree)
viz.GetProperty(Treebody).SetColor(255,255,0)
viz.start()
