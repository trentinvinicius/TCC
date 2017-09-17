import ode
import numpy as np
from math import cos, sin, pi, atan2, sqrt
from constants import *

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
        #create front right motor
        self.frMotorRoll = ode.AMotor(self.world)
        self.frMotorRoll.attach(self.bodyCar, self.bodyRWR)
        self.frMotorRoll.setNumAxes(1)
        self.frMotorRoll.setAxis(0, 2, (0, 0, 1))
        self.frMotorRoll.enable()
        self.frMotorRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frMotorRoll.setParam(ode.ParamSuspensionERP, 0.8)

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
    def __init__(self, world, space, viz, numLanes, direction, laneMain):
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.direction = direction
        self.numLanes = float(numLanes)
        if (laneMain <= self.numLanes/2.0):
            self.zPos = -(self.numLanes/2.0 - laneMain + 0.5) * ROADSIZE
        else:
            self.zPos = (laneMain - self.numLanes/2 -1 + 0.5) * ROADSIZE
        self.size = ROADSIZE * self.numLanes
        self.yPos =  0.20834342658224672 - WHEELRADIUS + 0.01
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setBox(ROADDENSITY, ROADLENGTH, ROADHEIGHT, self.size)
        self.body.setMass(mass)
        self.geom = ode.GeomBox(self.space, (ROADLENGTH, ROADHEIGHT, self.size))
        self.geom.setBody(self.body)
        self.geom.setPosition((0,0, self.zPos))
        self.viz.addGeom(self.geom)
        self.viz.GetProperty(self.body).SetColor(ROADCOLOR)
        p = []
        for n in range(int(self.numLanes)):
            p.append((-100, self.yPos, self.zPos + (self.numLanes/2 - n) * ROADSIZE, 1500, self.yPos, self.zPos + (self.numLanes/2 - n) * ROADSIZE, 1))
        p.append((-100, self.yPos, self.zPos + self.numLanes/2 * ROADSIZE, 1500, self.yPos, self.zPos + self.numLanes/2 * ROADSIZE, 0))
        p.append((-100, self.yPos, self.zPos - self.numLanes/2 * ROADSIZE, 1500, self.yPos, self.zPos - self.numLanes/2 * ROADSIZE, 0))
        if (self.numLanes % 2 == 0):
            if (self.direction):
                p.append((-100,  self.yPos, self.zPos, 1500,  self.yPos, self.zPos, 0))
            else:
                p.append((-100,  self.yPos, self.zPos, 1500,  self.yPos, self.zPos, 0))
        self.viz.drawLines(p)

    def getSides(self):
        return (self.zPos + self.numLanes/2 * ROADSIZE, self.zPos - self.numLanes/2 * ROADSIZE)

class Person(object):
    def __init__(self, world, space, viz, position, velocity, road):
        '''Position is a (x, 0, z) vector referenced from the car center
           Velocity is a three component vector (vx, 0, vz)'''
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.position = position
        self.velocity = velocity
        self.road = road
        self.axis2 = (0,0,1)
        self.axis1 = (0,1,0)
        self.axis3 = (1,0,0)
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setCylinderTotal(75, 2, PERSONRADIUS, PERSONHEIGHT)
        geom = ode.GeomCylinder(self.space, PERSONRADIUS, PERSONHEIGHT)
        geom.setBody(self.body)
        x,y,z = self.position
        self.body.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.body.setPosition((x, y + PERSONHEIGHT/2 + SPHERERADIUS, z))
        self.viz.addGeom(geom)
        self.viz.GetProperty(self.body).SetColor(PERSONCOLOR)
        #create spheres
        self.w1, gw1 = self.createSphere(x + PERSONRADIUS - SPHERERADIUS, z)
        self.w2, gw2 = self.createSphere(x - PERSONRADIUS + SPHERERADIUS, z)
        #s3, gs3 = self.createSphere(x, z + PERSONRADIUS - SPHERERADIUS)
        self.s4, gs4 = self.createSphere(x, z - PERSONRADIUS + SPHERERADIUS)

        #create joints
        self.j1 = ode.Hinge2Joint(self.world)
        self.j1.attach(self.w1, self.body)
        self.j1.setAnchor((x + PERSONRADIUS - SPHERERADIUS, SPHERERADIUS, z))
        self.j1.setAxis1(self.axis3)
        self.j1.setAxis2(self.axis2)

        self.j2 = ode.Hinge2Joint(self.world)
        self.j2.attach(self.w2, self.body)
        self.j2.setAnchor((x - PERSONRADIUS + SPHERERADIUS, SPHERERADIUS, z))
        self.j2.setAxis1(self.axis3)
        self.j2.setAxis2(self.axis2)
        
        '''j3 = ode.Hinge2Joint(self.world)
        j3.attach(s3, self.body)
        j3.setAnchor((x, SPHERERADIUS, z + PERSONRADIUS - SPHERERADIUS))
        j3.setAxis1(self.axis3)
        j3.setAxis2(self.axis2)'''
        
        j4 = ode.Hinge2Joint(self.world)
        j4.attach(self.s4, self.body)
        j4.setAnchor((x, SPHERERADIUS, z - PERSONRADIUS + SPHERERADIUS))
        j4.setAxis1(self.axis3)
        j4.setAxis2(self.axis2)
        #add person and road to allGroups
        allGroups.append([self.w1, self.body])
        allGroups.append([self.w2, self.body])
        #allGroups.append([s3, self.body])
        allGroups.append([self.s4, self.body])

        allGroups.append([self.w1, self.road])
        allGroups.append([self.w2, self.road])
        #allGroups.append([s3, self.road])
        allGroups.append([self.s4, self.road])
        self.setLinearVelocity()

    def createSphere(self, sx, sz):
        sphere = ode.Body(self.world)
        mSphere = ode.Mass()
        mSphere.setSphere(PERSONDENSITY, SPHERERADIUS)
        sphere.setMass(mSphere)
        geomSphere = ode.GeomSphere(self.space, SPHERERADIUS)
        geomSphere.setBody(sphere)    
        sphere.setPosition((sx, SPHERERADIUS, sz))
        self.viz.addGeom(geomSphere)
        self.viz.GetProperty(sphere).SetColor(PERSONCOLOR)
        return sphere, geomSphere

    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinder(PERSONDENSITY, 3, SPHERERADIUS, SPHERERADIUS) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, SPHERERADIUS, SPHERERADIUS)
        geomWheel.setBody(wheel)    
        wheel.setPosition((wx, SPHERERADIUS, wz))
        self.viz.addGeom(geomWheel)
        self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        return wheel, geomWheel

    def setLinearVelocity(self):
        vx, vy, vz = self.velocity
        ang = atan2(vz, vx)
        print ang*180/pi, sqrt(vx**2 + vz**2) 
        ang = -ang
        '''self.j1.setParam(ode.paramLoStop, ang)
        self.j1.setParam(ode.paramHiStop, ang)
        self.j2.setParam(ode.paramLoStop, ang)
        self.j2.setParam(ode.paramHiStop, ang)'''
        self.w1.setLinearVel((vx, vy, vz))
        self.w2.setLinearVel((vx, vy, vz))
        self.s4.setLinearVel((vx, vy, vz))
        #self.w1.setRotation((cos(ang), 0, sin(ang), 0, 1, 0, -sin(ang), 0 , cos(ang)))
        #self.w2.setRotation((cos(ang), 0, sin(ang), 0, 1, 0, -sin(ang), 0 , cos(ang)))
        #self.w1.setLinearVel((10,0,5))
        #self.w2.setLinearVel((10,0,5))
        #self.body.setLinearVel((vx, vy, vz))


class TreePole(object):
    def __init__(self, world, space, viz, position, tree = True):
        '''Position is a (x, 0, z) vector referenced from the car center
           Velocity is a three component vector (vx, 0, vz)'''
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.position = position
        if tree:
            self.color = TREECOLOR
            self.d = TREEDENSITY
        else:
            self.color = POLECOLOR
            self.d = POLEDENSITY
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setCylinder(self.d, 2, TREEPOLERADIUS, TREEPOLEHEIGHT)
        geom = ode.GeomCylinder(self.space, TREEPOLERADIUS, TREEPOLEHEIGHT)
        geom.setBody(self.body)
        x,y,z = self.position
        self.body.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.body.setPosition((x, y + 1.25, z))
        self.viz.addGeom(geom)
        #self.viz.stlGeom(self.viz.GetObject(geom), 'Images/tree.stl')
        self.viz.GetProperty(self.body).SetColor(self.color)
