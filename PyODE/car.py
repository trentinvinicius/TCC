import ode
import odeViz.ode_visualization as ode_viz
import numpy as np

dt = 1.0/30
world = ode.World()
world.setGravity((0, -9.81, 0))
world.setERP(0.8)
world.setCFM(1E-5)
allGroups = []

#create Space
space = ode.Space()

# Create a plane geom which prevent the objects from falling forever
floor = ode.GeomPlane(space, (0, 1, 0), -4)

def createWheels(wx, wz):
	    global viz
	    wheel = ode.Body(world)
	    mWheel = ode.Mass()
	    mWheel.setCylinder(100, 3, 0.5, 1) #density, direction(1,2,3), r, h
	    wheel.setMass(mWheel)
	    geomWheel = ode.GeomCylinder(space, 0.5, 1)
	    geomWheel.setBody(wheel)
	    wheel.setPosition((wx, 0, wz ))
	    viz.addGeom(geomWheel)
	    viz.GetProperty(wheel).SetColor(1,0,0)
	    return wheel, geomWheel


contactgroup = ode.JointGroup()

def idlefunc():
    
    
    n = 2
    for _ in range(n):
        # Detect collisions and create contact joints
        

        space.collide((world,contactgroup), near_callback)

        # Simulation step
        world.step(dt/n)

        # Remove all contact joints
        contactgroup.empty()

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

bodyCar = ode.Body(world)
mCar = ode.Mass()
mCar.setBoxTotal(800, 1.5, .10, 3.0)
bodyCar.setMass(mCar)
geomCar = ode.GeomBox(space, (1.5, .1, 3))
geomCar.setBody(bodyCar)
#bodyCar.setPosition((0 + position[0], wheelRadius + carHeight/2 + position[1], 0 + position[2]))
viz.addGeom(geomCar)          
viz.GetProperty(bodyCar).SetColor(0,0,1)
w1, g1 = createWheels(-1, -1.5)
w2, g2 = createWheels(1, -1.5)
w3, g3 = createWheels(1, 1.5)
w4, g4 = createWheels(-1, 1.5)

j1 = ode.Hinge2Joint(world)
j1.setAnchor((-1, 0, -1.5) )
j1.setAxis1((0,1,0))
j1.setAxis2((-1,0,0))
j1.attach(bodyCar, w1)

j2 = ode.Hinge2Joint(world)
j2.setAnchor((1, 0, -1.5) )
j2.setAxis1((0,1,0))
j2.setAxis2((-1,0,0))
j2.attach(bodyCar, w2)

j3 = ode.Hinge2Joint(world)
j3.setAnchor((1, 0, 1.5) )
j3.setAxis1((0,1,0))
j3.setAxis2((1,0,0))
j3.attach(bodyCar, w3)

j4 = ode.Hinge2Joint(world)
j4.setAnchor((-1, 0, 1.5) )
j4.setAxis1((0,1,0))
j4.setAxis2((1,0,0))
j4.attach(bodyCar, w4)

allGroups.append([bodyCar, w1])
allGroups.append([bodyCar, w2])
allGroups.append([bodyCar, w3])
allGroups.append([bodyCar, w4])


viz.start()