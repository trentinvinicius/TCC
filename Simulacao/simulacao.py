import ode
import odeViz.ode_visualization as ode_viz
from math import pi, cos, sin
import numpy as np
from objects import *

#Definitions
fps = 30.0
dt = 1.0/fps

global allGroups

allGroups = []

class Car(object):
    def __init__(self, world, space, viz, road, passengers = 5, mainCar = True, position = (0.0, 0.0, 0.0), direction = 1):
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.passengers = passengers
        self.position = position
        self.direction = direction
        self.road = road
        if mainCar:
            self.bodyCarColor = MAINCARCOLOR
        else:
            self.bodyCarColor = CARCOLOR
        self.create()

    def create(self):
        #create body
        self.bodyCar = ode.Body(self.world)
        mCar = ode.Mass()
        mCar.setBoxTotal((self.passengers*PERSONWEIGHT + CARWEIGHT), CARLENGTH, CARHEIGHT, CARWIDTH - WHEELWIDTH)
        self.bodyCar.setMass(mCar)
        self.geomCar = ode.GeomBox(self.space, (CARLENGTH, CARHEIGHT, CARWIDTH - WHEELWIDTH))
        self.geomCar.setBody(self.bodyCar)
        self.bodyCar.setPosition((0 + self.position[0], WHEELRADIUS + CARHEIGHT/2 + self.position[1], 0 + self.position[2]))
        self.viz.addGeom(self.geomCar)          
        self.viz.GetProperty(self.bodyCar).SetColor(self.bodyCarColor)
        #create wheels
        if (self.direction == -1):
           self.bodyFWL, self.geomFWL = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyFWR, self.geomFWR = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
           self.bodyRWL, self.geomRWL = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyRWR, self.geomRWR = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
           #self.viz.stlGeom(self.viz.GetObject(self.geomCar), CARCOMINGFILE)
        else: #if (self.direction == 1):
           self.bodyFWL, self.geomFWL = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
           self.bodyFWR, self.geomFWR = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyRWL, self.geomRWL = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
           self.bodyRWR, self.geomRWR = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
           #self.viz.stlGeom(self.viz.GetObject(self.geomCar), CARGOINGFILE)
        self.viz.GetProperty(self.bodyFWL).SetColor(self.bodyCarColor)
        #create front left joint

        self.flJoint = ode.Hinge2Joint(self.world)
        self.flJoint.attach(self.bodyCar, self.bodyFWL)
        if (self.direction == 1):
           self.flJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        else:
           self.flJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.flJoint.setAxis2((0,0,1))
        self.flJoint.setAxis1((0,1,0))
        self.flJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJoint.setParam(ode.ParamSuspensionERP, 0.8)
        '''
        self.flJointRoll = ode.HingeJoint(self.world)
        self.flJointYaw  = ode.HingeJoint(self.world)
        flJointBody = ode.Body(self.world)
        nullMass1 = ode.Mass()
        nullMass1.setBox(0.01, 0.01, 0.01, 0.01)
        flJointBody.setMass(nullMass1)
        self.flJointRoll.attach(flJointBody, self.bodyFWL)
        self.flJointYaw.attach(self.bodyCar, flJointBody)
        if (self.direction == 1):
           self.flJointRoll.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
           self.flJointYaw.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        else:
           self.flJointRoll.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
           print ((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2])), self.bodyFWL.getPosition()
           self.flJointYaw.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.flJointRoll.setAxis((0,0,1))
        self.flJointYaw.setAxis((0,1,0))
        self.flJointRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJointRoll.setParam(ode.ParamSuspensionERP, 0.8)
        self.flJointYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJointYaw.setParam(ode.ParamSuspensionERP, 0.8)'''
        #create front right joint
        self.frJoint = ode.Hinge2Joint(self.world)
        self.frJoint.attach(self.bodyCar, self.bodyFWR)
        if (self.direction == 1):
           self.frJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        else:
           self.frJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        self.frJoint.setAxis2((0,0,1))
        self.frJoint.setAxis1((0,1,0))
        self.frJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJoint.setParam(ode.ParamSuspensionERP, 0.8)
        '''
        self.frJointRoll = ode.HingeJoint(self.world)
        self.frJointYaw  = ode.HingeJoint(self.world)
        frJointBody = ode.Body(self.world)
        nullMass2 = ode.Mass()
        nullMass2.setBox(0.01, 0.01, 0.01, 0.01)
        frJointBody.setMass(nullMass2)
        self.frJointRoll.attach(frJointBody, self.bodyFWR)
        self.frJointYaw.attach(self.bodyCar, frJointBody)
        if (self.direction == 1):
           self.frJointRoll.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
           self.frJointYaw.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        else:
           self.frJointRoll.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
           self.frJointYaw.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        self.frJointRoll.setAxis((0,0,1))
        self.frJointYaw.setAxis((0,1,0))
        self.frJointRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJointRoll.setParam(ode.ParamSuspensionERP, 0.8)
        self.frJointYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJointYaw.setParam(ode.ParamSuspensionERP, 0.8)'''
        #create rear left joint
        self.rlJoint = ode.HingeJoint(self.world)
        self.rlJoint.attach(self.bodyCar, self.bodyRWL)
        if (self.direction == 1):
           self.rlJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], -CARWIDTH/2 + self.position[2]))
        else:
           self.rlJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.rlJoint.setAxis((0,0,1))
        #create rear right joint
        self.rrJoint = ode.HingeJoint(self.world)
        self.rrJoint.attach(self.bodyCar, self.bodyRWR)
        if (self.direction == 1):
           self.rrJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        else:
           self.rrJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], -CARWIDTH/2 + self.position[2]))
        self.rrJoint.setAxis((0,0,1))
        # add Joints to allGroups
        allGroups.append([self.bodyFWL, self.bodyCar])
        allGroups.append([self.bodyFWR, self.bodyCar])
        allGroups.append([self.bodyRWL, self.bodyCar])
        allGroups.append([self.bodyRWR, self.bodyCar])
        #allGroups.append([self.bodyFWL, self.bodyFWR, self.bodyRWL, self.bodyRWR, nullMass2, nullMass1, self.bodyCar])

        #add Wheels and Road to allGroups
        '''allGroups.append([self.bodyFWL, self.road])
        allGroups.append([self.bodyFWR, self.road])
        allGroups.append([self.bodyRWL, self.road])
        allGroups.append([self.bodyRWR, self.road])'''
        #create front left motor
        self.flMotorRoll = ode.AMotor(self.world)
        self.flMotorRoll.attach(self.bodyCar, self.bodyFWL)
        self.flMotorRoll.setNumAxes(1)
        self.flMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.flMotorRoll.enable()      
        self.flMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right motor
        self.frMotorRoll = ode.AMotor(self.world)
        self.frMotorRoll.attach(self.bodyCar, self.bodyFWR)
        self.frMotorRoll.setNumAxes(1)
        self.frMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.frMotorRoll.enable()
        self.frMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)
        #create rear left motor
        self.rlMotorRoll = ode.AMotor(self.world)
        self.rlMotorRoll.attach(self.bodyCar, self.bodyRWL)
        self.rlMotorRoll.setNumAxes(1)
        self.rlMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.rlMotorRoll.enable()      
        self.rlMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.rlMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)
        #create rear right motor
        self.rrMotorRoll = ode.AMotor(self.world)
        self.rrMotorRoll.attach(self.bodyCar, self.bodyRWR)
        self.rrMotorRoll.setNumAxes(1)
        self.rrMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.rrMotorRoll.enable()
        self.rrMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.rrMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)

    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinderTotal(WHEELWEIGHT, 3, WHEELRADIUS, WHEELWIDTH) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, WHEELRADIUS, WHEELWIDTH)
        geomWheel.setBody(wheel)    
    
        wheel.setPosition((wx + self.position[0], WHEELRADIUS  + self.position[1], wz + self.position[2]))
        self.viz.addGeom(geomWheel)
        self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        return wheel, geomWheel

    def setLinearVelocity(self, velocity):
        vx = self.direction*velocity
        self.bodyCar.setLinearVel((vx, 0, 0))
        
        print self.flJointRoll.getParam(ode.ParamFMax2)
        self.flJointRoll.setParam(ode.ParamFMax2,1000)
        print self.flJointRoll.getParam(ode.ParamFMax2),    "a"


        self.flMotorRoll.setParam(ode.ParamFMax, 10000)
        # print 'a', self.flMotorRoll.getParam(ode.ParamFMax)
        self.frMotorRoll.setParam(ode.ParamFMax, 10000)
        self.rlMotorRoll.setParam(ode.ParamFMax, 10000)
        self.rrMotorRoll.setParam(ode.ParamFMax, 10000)
        
        self.flMotorRoll.setParam(ode.ParamVel, vx)
        self.frMotorRoll.setParam(ode.ParamVel, vx)
        self.rlMotorRoll.setParam(ode.ParamVel, vx)
        self.rrMotorRoll.setParam(ode.ParamVel, vx)

        #self.bodyFWL.setLinearVel((vx,0,0))
        

    def getLinearVelocity(self):
        return self.bodyCar.getLinearVel()
        
    def addTorque(self, torque):
        self.flMotorRoll.addTorques(torque, 0.0, 0.0)
        self.frMotorRoll.addTorques(torque, 0.0, 0.0)

    def setSteerAngle(self, ang):
        if (ang < MINSTEERANGLE):
            ang = MINSTEERANGLE
        if (ang > MAXSTEERANGLE):
            ang = MAXSTEERANGLE

        ang *= pi/180.0
        self.flJointYaw.setParam(ode.paramLoStop, ang)
        self.flJointYaw.setParam(ode.paramHiStop, ang)
        self.frJointYaw.setParam(ode.paramLoStop, ang)
        self.frJointYaw.setParam(ode.paramHiStop, ang)

    def getSteerAngle(self):
        #print self.flJoint.getAngle1Rate()
        return (28.64788975654116*(self.flJoint.getParam(ode.paramHiStop) + self.flJoint.getParam(ode.paramLoStop)), \
                28.64788975654116*(self.frJoint.getParam(ode.paramHiStop) + self.frJoint.getParam(ode.paramLoStop)))   # 28.64788975654116 = 0.5 * 180/pi

    def getPosition(self):
        return self.bodyCar.getPosition()

    def brake(self):
        rBrakeForce = 250.0
        fBrakeForce = 500.0
        self.flJoint.setParam(ode.ParamVel2, 0.0)
        print "abcd", self.flJoint.getParam(ode.ParamFMax)
        self.flJoint.setParam(ode.ParamFMax2, fBrakeForce)
        print "abc", self.flJoint.getParam(ode.ParamFMax)
        self.frJoint.setParam(ode.ParamVel2, 0.0)
        self.frJoint.setParam(ode.ParamFMax2, fBrakeForce)
        self.rlJoint.setParam(ode.ParamVel2, 0.0)
        self.rlJoint.setParam(ode.ParamFMax2, rBrakeForce)
        self.rrJoint.setParam(ode.ParamVel2, 0.0)
        self.rrJoint.setParam(ode.ParamFMax2, rBrakeForce)



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
    #c2.setSteerAngle(0.0)
    #c2.setLinearVelocity(10)
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
c2 = Car(world, [space], viz, road = 1)
viz.start()
