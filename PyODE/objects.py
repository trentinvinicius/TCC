import ode
import numpy as np
from math import cos, sin, pi
from constants import *
import vtk

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
        self.bodyFWL, self.geomFWL = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
        self.bodyFWR, self.geomFWR = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
        self.bodyRWL, self.geomRWL = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
        self.bodyRWR, self.geomRWR = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
        #create front left joint
        self.flJoint = ode.Hinge2Joint(self.world)
        self.flJoint.attach(self.bodyCar, self.bodyFWL)
        self.flJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        self.flJoint.setAxis2((0,0,1))
        self.flJoint.setAxis1((0,1,0))
        self.flJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJoint.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right joint
        self.frJoint = ode.Hinge2Joint(self.world)
        self.frJoint.attach(self.bodyCar, self.bodyFWR)
        self.frJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.frJoint.setAxis2((0,0,1))
        self.frJoint.setAxis1((0,1,0))
        self.frJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJoint.setParam(ode.ParamSuspensionERP, 0.8)
        #create rear left joint
        self.rlJoint = ode.HingeJoint(self.world)
        self.rlJoint.attach(self.bodyCar, self.bodyRWL)
        self.rlJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], -CARWIDTH/2 + self.position[2]))
        self.rlJoint.setAxis((0,0,1))
        #create rear right joint
        self.rrJoint = ode.HingeJoint(self.world)
        self.rrJoint.attach(self.bodyCar, self.bodyRWR)
        self.rrJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.rrJoint.setAxis((0,0,1))
        # add Joints to allGroups
        allGroups.append([self.bodyFWL, self.bodyCar])
        allGroups.append([self.bodyFWR, self.bodyCar])
        allGroups.append([self.bodyRWL, self.bodyCar])
        allGroups.append([self.bodyRWR, self.bodyCar])
        #add Wheels and Road to allGroups
        allGroups.append([self.bodyFWL, self.road])
        allGroups.append([self.bodyFWR, self.road])
        allGroups.append([self.bodyRWL, self.road])
        allGroups.append([self.bodyRWR, self.road])
        #create front left motor roll
        self.flMotorRoll = ode.AMotor(self.world)
        self.flMotorRoll.attach(self.bodyCar, self.bodyRWL)
        self.flMotorRoll.setNumAxes(1)
        self.flMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.flMotorRoll.enable()      
        self.flMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)
        #create front left motor yaw
        self.flMotorYaw = ode.AMotor(self.world)
        self.flMotorYaw.attach(self.bodyCar, self.bodyRWL)
        self.flMotorYaw.setNumAxes(1)
        self.flMotorYaw.setAxis(0, 2, (0, 1, 0))
        self.flMotorYaw.enable()     
        self.flMotorYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flMotorYaw.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right motor
        self.frMotorRoll = ode.AMotor(self.world)
        self.frMotorRoll.attach(self.bodyCar, self.bodyRWR)
        self.frMotorRoll.setNumAxes(1)
        self.frMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.frMotorRoll.enable()
        self.frMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right motor
        self.frMotorYaw = ode.AMotor(self.world)
        self.frMotorYaw.attach(self.bodyCar, self.bodyRWR)
        self.frMotorYaw.setNumAxes(1)
        self.frMotorYaw.setAxis(0, 2, (0, 1, 0))
        self.frMotorYaw.enable()
        self.frMotorYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frMotorYaw.setParam(ode.ParamSuspensionERP, 0.8)

    def createWheels(self, wx, wz, r = 0, l = 0):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinder(100, 3, WHEELRADIUS + r, WHEELWIDTH + l) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, WHEELRADIUS + r, WHEELWIDTH +l)
        geomWheel.setBody(wheel)    
        wheel.setPosition((wx + self.position[0], WHEELRADIUS  + self.position[1], wz + self.position[2]))
        self.viz.addGeom(geomWheel)
        self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        return wheel, geomWheel

    def setLinearVelocity(self, velocity):
        vx, vy, vz = self.direction*np.array(velocity)
        self.bodyCar.setLinearVel((vx, vy, vz))

    def addTorque(self, torque):
        self.flMotorRoll.addTorques(torque, 0.0, 0.0)
        self.frMotorRoll.addTorques(torque, 0.0, 0.0)

    def setSteerAngle(self, ang):
        if (ang < MINSTEERANGLE):
            ang = MINSTEERANGLE
        if (ang > MAXSTEERANGLE):
            ang = MAXSTEERANGLE
        self.flJoint.setParam(ode.paramLoStop, ang)
        self.flJoint.setParam(ode.paramHiStop, ang)
        self.frJoint.setParam(ode.paramLoStop, ang)
        self.frJoint.setParam(ode.paramHiStop, ang)

    def getSteerAngle(self):
        print self.flJoint.getAngle1Rate()
        return (28.64788975654116*(self.flJoint.getParam(ode.paramHiStop) + self.flJoint.getParam(ode.paramLoStop)), \
                28.64788975654116*(self.frJoint.getParam(ode.paramHiStop) + self.frJoint.getParam(ode.paramLoStop)))   # 28.64788975654116 = 0.5 * 180/pi

    def getPosition(self):
        return self.bodyCar.getPosition()

class Road(object):
    def __init__(self, world, space, viz, numLanes):
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.size = ROADSIZE * numLanes
        self.create()

    def create(self):
        self.road = ode.Body(self.world)
        mRoad = ode.Mass()
        mRoad.setBox(1, 3000, 0.01, self.size)
        self.road.setMass(mRoad)
        self.geomRoad = ode.GeomBox(self.space, (3000, 0.01, self.size))
        self.geomRoad.setBody(self.road)
        self.geomRoad.setPosition((0,0,0))
        self.viz.addGeom(self.geomRoad)
        self.reader = vtk.vtkJPGReader()
        self.reader.SetFileName(WHEEL_IMAGE)
        self.texture = vtk.vtkTexture()
        transform = vtk.vtkTransform()
        transform.Scale(1.0,1.0,1.0)
        self.texture.SetTransform(transform)
        self.viz.GetProperty(self.road).SetColor(ROADCOLOR)

class Person(object):
    def __init__(self, world, space, viz, position, velocity):
        '''Position is a (x, 0, z) vector referenced from the car center
           Velocity is a three component vector (vx, 0, vz)'''
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.position = position
        self.velocity = velocity
        self.personColor = 146.0/255, 54.0/255, 252.0/255
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setCylinder(100, 2, 0.4, 1.8)
        mass.setSphere(100,4)
        geom = ode.GeomCylinder(self.space, 0.4, 1.8)
        geom = ode.GeomSphere(self.space, 4)
        geom.setBody(self.body)
        x,y,z = self.position
        self.body.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.body.setPosition((x, y + 0.9, z))
        self.viz.addGeom(geom)
        self.viz.GetProperty(self.body).SetColor(self.personColor)
        self.setLinearVelocity()

    def setLinearVelocity(self):
        vx, vy, vz = self.velocity
        self.body.setLinearVel((vx, vy, vz))

class TreePole(object):
    def __init__(self, world, space, viz, position, tree = True):
        '''Position is a (x, 0, z) vector referenced from the car center
           Velocity is a three component vector (vx, 0, vz)'''
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.position = position
        if tree:
            self.color = 125.0/255, 65.0/255, 39.0/255
            self.d = 600
        else:
            self.color = 211.0/255, 211.0/255, 211.0/255
            self.d = 2500
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setCylinder(self.d, 2, 0.3, 2.5)
        geom = ode.GeomCylinder(self.space, 0.3, 2.5)
        geom.setBody(self.body)
        x,y,z = self.position
        self.body.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.body.setPosition((x, y + 1.25, z))
        self.viz.addGeom(geom)
        self.viz.GetProperty(self.body).SetColor(self.treeColor)
