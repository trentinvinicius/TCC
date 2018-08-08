import ode
import numpy as np
from math import cos, sin, pi, atan2, sqrt
from constants import *

allGroups = []

class Car(object):
    def __init__(self, world, space, viz, dist, passengers = MAXPASSANGERS, mainCar = True, position = (0.0, 0.0, 0.0), direction = 1, num = 0, color = 2):
        self.world = world
        self.space = space
        self.viz = viz
        self.passengers = passengers
        self.direction = direction
        if self.direction == 1:
            self.position = np.array(position) - np.array((dist, 0, 0))
        else:
            self.position = np.array(position) + np.array((dist, 0, 0))
        if mainCar:
            if color == 0:
                self.bodyCarColor = MAINCARCOLOR
            else:
                self.bodyCarColor = 0.2, 0.6, 0.4

            self.name = "MainCar"
            self.nameWheel = "MainCarWheel"
        else:
            self.bodyCarColor = CARCOLOR
            self.name = "OtherCar" + str(num)
            self.nameWheel = "OtherCarWheel" + str(num)
        self.create()

    def create(self):
        a =  1#-2 # 1
        #create body
        self.bodyCar = ode.Body(self.world)
        mCar = ode.Mass()
        mCar.setBoxTotal((self.passengers*PERSONWEIGHT + CARWEIGHT), CARLENGTH, CARHEIGHT, CARWIDTH - a*WHEELWIDTH)
        self.bodyCar.setMass(mCar)
        if self.direction == -1:
            #pass
            self.bodyCar.setRotation((cos(pi), 0, sin(pi), 0, 1, 0, -sin(pi), 0, cos(pi)))
        self.geomCar = ode.GeomBox(self.space, (CARLENGTH, CARHEIGHT, CARWIDTH - a*WHEELWIDTH))
        self.geomCar.setBody(self.bodyCar)
        self.bodyCar.setPosition((self.position[0], BASEHEIGHT + WHEELRADIUS + CARHEIGHT/2 + self.position[1], self.position[2]))
        if self.viz:
            self.viz.addGeom(self.geomCar)          
            self.viz.GetProperty(self.bodyCar).SetColor(self.bodyCarColor)
        #create wheels
        if (self.direction == -1):
           self.bodyFWL, self.geomFWL = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyFWR, self.geomFWR = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
           self.bodyRWL, self.geomRWL = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyRWR, self.geomRWR = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
           if self.viz:
            #pass
            self.viz.stlGeom(self.viz.GetObject(self.geomCar), CARGOINGFILE)
        else: #if (self.direction == 1):
           self.bodyFWL, self.geomFWL = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
           self.bodyFWR, self.geomFWR = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyRWL, self.geomRWL = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
           self.bodyRWR, self.geomRWR = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
           if self.viz:
            #pass
            self.viz.stlGeom(self.viz.GetObject(self.geomCar), CARGOINGFILE)
        #create front left joints
        self.flJointRoll = ode.HingeJoint(self.world)
        self.flJointYaw  = ode.HingeJoint(self.world)
        self.flJointBody = ode.Body(self.world)
        self.nullMass1 = ode.Mass()
        self.nullMass1.setBox(0.01, 0.01, 0.01, 0.01)
        self.flJointBody.setMass(self.nullMass1)
        #self.geom1Test = ode.GeomBox(self.space, (0.01, 0.01, 0.01))
        #self.geom1Test.setBody(self.flJointBody)
        #self.geom1Test.__setattr__('name', "BOSTA")
        #self.geom1Test.setPosition((self.bodyFWL.getPosition()))
        self.flJointBody.setPosition((self.bodyFWL.getPosition()))

        self.flJointRoll.attach(self.flJointBody, self.bodyFWL)
        self.flJointYaw.attach(self.bodyCar, self.flJointBody)    
        self.flJointRoll.setAnchor((self.bodyFWL.getPosition()))
        self.flJointYaw.setAnchor((self.bodyFWL.getPosition()))
        self.flJointRoll.setAxis((0,0,1))
        self.flJointYaw.setAxis((0,1,0))
        self.flJointRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJointRoll.setParam(ode.ParamSuspensionERP, 0.8)
        self.flJointYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJointYaw.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right joints
        self.frJointRoll = ode.HingeJoint(self.world)
        self.frJointYaw  = ode.HingeJoint(self.world)
        self.frJointBody = ode.Body(self.world)
        self.nullMass2 = ode.Mass()
        self.nullMass2.setBox(0.01, 0.01, 0.01, 0.01)
        self.frJointBody.setMass(self.nullMass2)

        #self.geom2Test = ode.GeomBox(self.space, (0.01, 0.01, 0.01))
        #self.geom2Test.setBody(self.frJointBody)
        #self.geom2Test.__setattr__('name', "BOSTA")
        #self.geom2Test.setPosition((self.bodyFWR.getPosition()))
        self.frJointBody.setPosition((self.bodyFWR.getPosition()))

        self.frJointRoll.attach(self.frJointBody, self.bodyFWR)
        self.frJointYaw.attach(self.bodyCar, self.frJointBody)
        self.frJointRoll.setAnchor((self.bodyFWR.getPosition()))
        self.frJointYaw.setAnchor((self.bodyFWR.getPosition()))
        self.frJointRoll.setAxis((0,0,1))
        self.frJointYaw.setAxis((0,1,0))
        self.frJointRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJointRoll.setParam(ode.ParamSuspensionERP, 0.8)
        self.frJointYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJointYaw.setParam(ode.ParamSuspensionERP, 0.8)
        #create rear left joint
        self.rlJoint = ode.HingeJoint(self.world)
        self.rlJoint.attach(self.bodyCar, self.bodyRWL)
        self.rlJoint.setAnchor((self.bodyRWL.getPosition()))
        self.rlJoint.setAxis((0,0,1))
        #create rear right joint
        self.rrJoint = ode.HingeJoint(self.world)
        self.rrJoint.attach(self.bodyCar, self.bodyRWR)
        self.rrJoint.setAnchor((self.bodyRWR.getPosition()))
        self.rrJoint.setAxis((0,0,1))
        # add Bodies to allGroups
        allGroups.append([self.bodyFWL, self.bodyFWR, self.bodyRWL, self.bodyRWR, self.frJointBody, self.flJointBody, self.bodyCar, "Car"])
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
        self.flMotorRoll.setFeedback(True)
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
        #add name and body to group
        self.geomCar.__setattr__('name', self.name)

    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinderTotal(WHEELWEIGHT, 3, WHEELRADIUS, WHEELWIDTH) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, WHEELRADIUS, WHEELWIDTH)
        geomWheel.setBody(wheel)
        wheel.setPosition((wx + self.position[0], BASEHEIGHT + WHEELRADIUS  + self.position[1], wz + self.position[2]))
        if self.viz:
            self.viz.addGeom(geomWheel)
            self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        geomWheel.__setattr__('name', self.nameWheel)
        return wheel, geomWheel

    def setLinearVelocity(self, velocity):
        MAXFORCE = 10000
        vx = (self.direction*velocity)/WHEELRADIUS
        #self.bodyCar.setLinearVel((vx, 0, 0))
        #setting maximal force on the motors
        self.flMotorRoll.setParam(ode.ParamFMax, MAXFORCE)
        self.frMotorRoll.setParam(ode.ParamFMax, MAXFORCE)
        self.rlMotorRoll.setParam(ode.ParamFMax, MAXFORCE)
        self.rrMotorRoll.setParam(ode.ParamFMax, MAXFORCE)
        #setting velocity
        self.flMotorRoll.setParam(ode.ParamVel, vx)
        self.frMotorRoll.setParam(ode.ParamVel, vx)
        self.rlMotorRoll.setParam(ode.ParamVel, vx)
        self.rrMotorRoll.setParam(ode.ParamVel, vx)

    def getWheelPosition(self):
        return self.bodyFWL.getPosition(), self.bodyFWR.getPosition(), \
               self.bodyRWL.getPosition(), self.bodyRWR.getPosition()
        
    def getLinearVelocity(self):
        return np.linalg.norm(self.bodyCar.getLinearVel())
        
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
        return (28.64788975654116*(self.flJointYaw.getParam(ode.paramHiStop) + self.flJointYaw.getParam(ode.paramLoStop)), \
                28.64788975654116*(self.frJointYaw.getParam(ode.paramHiStop) + self.frJointYaw.getParam(ode.paramLoStop)))   # 28.64788975654116 = 0.5 * 180/pi

    def getPosition(self):
        return self.bodyCar.getPosition()

    def inPosition(self):
        aux = self.getPosition()[0]
        if (aux > 0 and int(aux) == 0):
            return True
        return False

    def brake(self, force):
        self.flMotorRoll.setParam(ode.ParamFMax, 0)
        self.frMotorRoll.setParam(ode.ParamFMax, 0)
        self.rlMotorRoll.setParam(ode.ParamFMax, 0)
        self.rrMotorRoll.setParam(ode.ParamFMax, 0)

        '''rBrakeForce = forces[0]
        fBrakeForce = forces[1]
        self.flJointRoll.setParam(ode.ParamVel, 0.0)
        self.flJointRoll.setParam(ode.ParamFMax, fBrakeForce)
        self.frJointRoll.setParam(ode.ParamVel, 0.0)
        self.frJointRoll.setParam(ode.ParamFMax, fBrakeForce)
        self.rlJoint.setParam(ode.ParamVel, 0.0)
        self.rlJoint.setParam(ode.ParamFMax, rBrakeForce)
        self.rrJoint.setParam(ode.ParamVel, 0.0)
        self.rrJoint.setParam(ode.ParamFMax, rBrakeForce)
        '''
        self.flJointRoll.setParam(ode.ParamVel, 0.0)
        self.flJointRoll.setParam(ode.ParamFMax, force)
        self.frJointRoll.setParam(ode.ParamVel, 0.0)
        self.frJointRoll.setParam(ode.ParamFMax, force)
        self.rlJoint.setParam(ode.ParamVel, 0.0)
        self.rlJoint.setParam(ode.ParamFMax, force)
        self.rrJoint.setParam(ode.ParamVel, 0.0)
        self.rrJoint.setParam(ode.ParamFMax, force)

    def getJointsVelocity(self):
        return self.flJointRoll.getParam(ode.ParamVel), self.frJointRoll.getParam(ode.ParamVel), \
               self.rlJoint.getParam(ode.ParamVel), self.rrJoint.getParam(ode.ParamVel)

    def carInfo(self):
        print self.getPosition(), self.getLinearVelocity(), self.getSteerAngle()
        print self.getWheelPosition()
        print self.getJointsVelocity()

class Road(object):
    def __init__(self, world, space, viz, numLanes, direction, laneMain, crossPos, statusSemaphore):
        self.world = world
        self.space = space
        self.viz = viz
        self.direction = direction
        self.numLanes = float(numLanes)
        if (laneMain <= self.numLanes/2.0):
            self.zPos = -(self.numLanes/2.0 - laneMain + 0.5) * ROADSIZE
        else:
            self.zPos = (laneMain - self.numLanes/2.0 - 1 + 0.5) * ROADSIZE
        self.size = ROADSIZE * self.numLanes
        self.yPos =  0.20834342658224672 - WHEELRADIUS + ROADHEIGHT# + BASEHEIGHT/2
        self.crossPos = crossPos
        self.statusSemaphore = statusSemaphore
        self.create()

    def create(self):
        #self.body = ode.Body(self.world)
        #mass = ode.Mass()
        #mass.setBox(ROADDENSITY, ROADLENGTH, ROADHEIGHT, self.size)
        #self.body.setMass(mass)
        self.geom = ode.GeomBox(self.space, (ROADLENGTH, ROADHEIGHT, self.size))
        #self.geom.setBody(self.body)
        self.geom.setPosition((ROADLENGTH/2 - 500.0 , BASEHEIGHT/2, self.zPos))
        if self.viz:
            self.viz.addGeom(self.geom)
            self.viz.GetProperty(self.geom).SetColor(ROADCOLOR)
            #draw lines on the road
            p = []
            d = 0.1
            for n in range(int(self.numLanes)):
                p.append((-500, self.yPos + d, self.zPos + (self.numLanes/2 - n) * ROADSIZE, 1500, self.yPos, self.zPos + (self.numLanes/2 - n) * ROADSIZE, 1))
            p.append((-500, self.yPos + d, self.zPos + self.numLanes/2 * ROADSIZE, 1500, self.yPos, self.zPos + self.numLanes/2 * ROADSIZE, 0))
            p.append((-500, self.yPos + d, self.zPos - self.numLanes/2 * ROADSIZE, 1500, self.yPos, self.zPos - self.numLanes/2 * ROADSIZE, 0))
            if (self.numLanes % 2 == 0):
                if (self.direction):
                    p.append((-500,  self.yPos + d, self.zPos, 1500,  self.yPos, self.zPos, 0))
                else:
                    p.append((-500,  self.yPos + d, self.zPos, 1500,  self.yPos, self.zPos, 1))
            self.viz.drawLines(p)
            #draw crosswalk
            if (self.crossPos > 0):
                c = []
                for n in range(int(self.numLanes)*10 + 2):
                    if (n%2 == 0):
                        c.append((self.crossPos - 1.0, self.yPos + d, (self.zPos - self.numLanes/2 * ROADSIZE) + n * CROSSWALKSIDE, \
                                  self.crossPos + 1.0, self.yPos + d, (self.zPos - self.numLanes/2 * ROADSIZE) + n * CROSSWALKSIDE, 0))
                self.viz.drawLines(c, 10)
        if (self.crossPos > 0):
            self.s = Semaphore(self.world, self.space, self.viz, (self.crossPos - 1.5, 0, self.getSides()[0] + 1), self.statusSemaphore)

        self.geom.__setattr__('name','Road')

    def getSides(self):
        return (self.zPos + self.numLanes/2.0 * ROADSIZE, self.zPos - self.numLanes/2.0 * ROADSIZE)

class Person(object):
    def __init__(self, world, space, viz, position, velocity, orientation, gender, age, num): 
        '''Position is a (x, 0, z) vector referenced from the car center
           Velocity is a three component vector (vx, 0, vz)'''
        self.world = world
        self.space = space
        self.viz = viz
        self.position = position
        self.ang = float(orientation)*pi/180
        self.velocity = velocity
        self.gender = gender
        self.age = age
        self.scaleMass = 1.0
        self.scale = 1.0
        if (self.gender  == 0): # Male
            if self.age == 0:
                self.stlFile = "Images/boy.obj"
                self.color = (0.4, 0.4, 1)
                self.scale = 0.71
                self.scaleMass = 0.5
                self.type = "MaleKid"
            elif self.age == 1:
                self.stlFile = "Images/man.obj" 
                self.color = (0, 0, 1)
                self.type = "MaleAdult"
            else:
                self.stlFile = "Images/oldman.obj"
                self.color = (0, 0, 0.6)
                self.type = "MaleElderly"
        else: # Female
            if self.age == 0:
                self.stlFile = "Images/girl.obj"
                self.color = (1, 0.4, 0.4)
                self.scale = 0.71
                self.scaleMass = 0.5
                self.type = "FemaleKid"
            elif self.age == 1:
                self.stlFile = "Images/woman.obj" 
                self.color = (1, 0, 0)
                self.type = "FemaleAdult"
            else:
                self.stlFile = "Images/oldwoman.obj"
                self.color = (0.6, 0, 0)
                self.type = "FemaleElderly"
        self.num = num
        self.create()

    def create(self):
        b = 2#3 #2
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setBoxTotal(self.scaleMass * PERSONWEIGHT, self.scale * PERSONRADIUS*2, self.scale * PERSONHEIGHT, self.scale * PERSONRADIUS*2)
        self.body.setMass(mass)
        self.geom = ode.GeomBox(self.space, (self.scale * PERSONRADIUS*b, self.scale * PERSONHEIGHT, self.scale * PERSONRADIUS*b))
        self.geom.setBody(self.body)
        x,y,z = self.position
        self.body.setRotation((cos(self.ang), 0, sin(self.ang), 0, 1, 0, -sin(self.ang), 0, cos(self.ang)))
        self.body.setPosition((self.position[0], BASEHEIGHT + self.position[1] + self.scale * PERSONHEIGHT/2 + SPHERERADIUS, self.position[2]))
        if self.viz:
            self.viz.addGeom(self.geom)
            self.viz.GetProperty(self.body).SetColor(PERSONCOLOR)
            if self.stlFile != None:
                self.viz.objGeom(self.viz.GetObject(self.geom), self.stlFile)
                self.viz.GetProperty(self.geom).SetColor(self.color)
      
        #create spheres
        self.w1, self.gw1 = self.createWheels( self.scale * PERSONRADIUS*cos(self.ang) - self.scale * PERSONRADIUS*sin(self.ang),  self.scale * PERSONRADIUS*(-sin(self.ang)) - self.scale * PERSONRADIUS*cos(self.ang))
        self.w2, self.gw2 = self.createWheels( self.scale * PERSONRADIUS*cos(self.ang) + self.scale * PERSONRADIUS*sin(self.ang),  self.scale * PERSONRADIUS*(-sin(self.ang)) + self.scale * PERSONRADIUS*cos(self.ang))
        self.w3, self.gw3 = self.createWheels(-self.scale * PERSONRADIUS*cos(self.ang) - self.scale * PERSONRADIUS*sin(self.ang), -self.scale * PERSONRADIUS*(-sin(self.ang)) - self.scale * PERSONRADIUS*cos(self.ang))
        self.w4, self.gw4 = self.createWheels(-self.scale * PERSONRADIUS*cos(self.ang) + self.scale * PERSONRADIUS*sin(self.ang), -self.scale * PERSONRADIUS*(-sin(self.ang)) + self.scale * PERSONRADIUS*cos(self.ang))
        #create joints
        axis = (sin(self.ang), 0, cos(self.ang))
        self.j1 = ode.HingeJoint(self.world)
        self.j1.attach(self.body, self.w1)
        self.j1.setAnchor((self.w1.getPosition()))
        self.j1.setAxis(axis)
        self.j2 = ode.HingeJoint(self.world)
        self.j2.attach(self.body, self.w2)
        self.j2.setAnchor((self.w2.getPosition()))
        self.j2.setAxis(axis)
        self.j3 = ode.HingeJoint(self.world)
        self.j3.attach(self.body, self.w3)
        self.j3.setAnchor((self.w3.getPosition()))
        self.j3.setAxis(axis)
        self.j4 = ode.HingeJoint(self.world)
        self.j4.attach(self.body, self.w4)
        self.j4.setAnchor((self.w4.getPosition()))
        self.j4.setAxis(axis)
        #add body and wheels to allGroups
        allGroups.append([self.w1, self.w2, self.w3, self.w4, self.body, "Pessoa"])
        name = "Person" + self.type + str(self.num)
        self.geom.__setattr__('name', name)

        self.setLinearVelocity()
        
    def createSphere(self, sx, sz):
        sphere = ode.Body(self.world)
        mSphere = ode.Mass()
        mSphere.setSphere(PERSONDENSITY, SPHERERADIUS)
        sphere.setMass(mSphere)
        geomSphere = ode.GeomSphere(self.space, SPHERERADIUS)
        geomSphere.setBody(sphere)    
        sphere.setPosition((sx + self.position[0], BASEHEIGHT + SPHERERADIUS + self.position[1], sz + self.position[2]))
        if self.viz:
            self.viz.addGeom(geomSphere)
            self.viz.GetProperty(sphere).SetColor(PERSONCOLOR)
        name = "PersonSphere" + str(self.num)
        geomSphere.__setattr__('name', name)
        return sphere, geomSphere

    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinderTotal(1.0, 3, SPHERERADIUS, SPHERERADIUS) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, SPHERERADIUS, SPHERERADIUS)
        geomWheel.setBody(wheel)    
        wheel.setPosition((wx + self.position[0], BASEHEIGHT + SPHERERADIUS  + self.position[1], wz + self.position[2]))
        wheel.setRotation((cos(self.ang), 0, sin(self.ang), 0, 1, 0, -sin(self.ang), 0, cos(self.ang)))
        name = "Person" + self.type + "Wheel" + str(self.num)
        geomWheel.__setattr__('name', name)
        if self.viz and False:
            self.viz.addGeom(geomWheel)
            self.viz.GetProperty(wheel).SetColor((1,0,0))
        return wheel, geomWheel

    def setLinearVelocity(self): 
        self.j4.setParam(ode.ParamFMax, 5)
        self.j3.setParam(ode.ParamFMax, 5)
        self.j4.setParam(ode.ParamVel, self.velocity/SPHERERADIUS)
        self.j3.setParam(ode.ParamVel, self.velocity/SPHERERADIUS)

    def getPosition(self):
        return self.body.getPosition()

class Animal(object):
    def __init__(self, world, space, viz, position, velocity, orientation, num):
        self.world = world
        self.space = space
        self.viz = viz
        self.position = position
        self.ang = float(orientation)*pi/180.0
        self.velocity = velocity
        self.num = num
        self.create()

    def create(self):
        c =1#  1.5 #1
        #create body
        self.bodyAnimal = ode.Body(self.world)
        mAnimal = ode.Mass()
        mAnimal.setBoxTotal(ANIMALWEIGHT, ANIMALLENGTH, ANIMALHEIGHT, ANIMALWIDTH - ANIMALWHEELWIDTH)
        self.bodyAnimal.setMass(mAnimal)
        self.geomAnimal = ode.GeomBox(self.space, (ANIMALLENGTH*c, ANIMALHEIGHT, c*ANIMALWIDTH - ANIMALWHEELWIDTH))
        self.geomAnimal.setBody(self.bodyAnimal)
        self.bodyAnimal.setPosition((self.position[0], BASEHEIGHT + ANIMALWHEELRADIUS + ANIMALHEIGHT/2 + self.position[1], self.position[2]))
        self.bodyAnimal.setRotation((cos(self.ang), 0, sin(self.ang), 0, 1, 0, -sin(self.ang), 0, cos(self.ang)))
        if self.viz:
            self.viz.addGeom(self.geomAnimal)
            self.viz.stlGeom(self.viz.GetObject(self.geomAnimal), ANIMALFILE)
            self.viz.GetProperty(self.geomAnimal).SetColor(ANIMALCOLOR)

        name = "Animal" + str(self.num)
        self.geomAnimal.__setattr__('name', name)         
        #create wheels
        self.bodyFWL, self.geomFWL = self.createWheels( ANIMALLENGTH/2*cos(self.ang) - ANIMALWIDTH/2*sin(self.ang),  ANIMALLENGTH/2*(-sin(self.ang)) - ANIMALWIDTH/2*cos(self.ang))
        self.bodyFWR, self.geomFWR = self.createWheels( ANIMALLENGTH/2*cos(self.ang) + ANIMALWIDTH/2*sin(self.ang),  ANIMALLENGTH/2*(-sin(self.ang)) + ANIMALWIDTH/2*cos(self.ang))
        self.bodyRWL, self.geomRWL = self.createWheels(-ANIMALLENGTH/2*cos(self.ang) - ANIMALWIDTH/2*sin(self.ang), -ANIMALLENGTH/2*(-sin(self.ang)) - ANIMALWIDTH/2*cos(self.ang))
        self.bodyRWR, self.geomRWR = self.createWheels(-ANIMALLENGTH/2*cos(self.ang) + ANIMALWIDTH/2*sin(self.ang), -ANIMALLENGTH/2*(-sin(self.ang)) + ANIMALWIDTH/2*cos(self.ang))
        #add to allGroups
        allGroups.append([self.bodyAnimal, self.bodyFWL, self.bodyFWR, self.bodyRWL, self.bodyRWR, "Animal"])
        #create front left joint
        axis = (sin(self.ang), 0, cos(self.ang))
        self.flJoint = ode.HingeJoint(self.world)
        self.flJoint.attach(self.bodyAnimal, self.bodyFWL)
        self.flJoint.setAnchor((self.bodyFWL.getPosition()))
        self.flJoint.setAxis(axis)
        #create front right joint
        self.frJoint = ode.HingeJoint(self.world)
        self.frJoint.attach(self.bodyAnimal, self.bodyFWR)
        self.frJoint.setAnchor((self.bodyFWR.getPosition()))
        self.frJoint.setAxis(axis)
        #create rear left joint
        self.rlJoint = ode.HingeJoint(self.world)
        self.rlJoint.attach(self.bodyAnimal, self.bodyRWL)
        self.rlJoint.setAnchor((self.bodyRWL.getPosition()))
        self.rlJoint.setAxis(axis)
        #create rear right joint
        self.rrJoint = ode.HingeJoint(self.world)
        self.rrJoint.attach(self.bodyAnimal, self.bodyRWR)
        self.rrJoint.setAnchor((self.bodyRWR.getPosition()))
        self.rrJoint.setAxis(axis)

        self.setLinearVelocity()


    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinderTotal(1.0, 3, ANIMALWHEELRADIUS, ANIMALWHEELWIDTH) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, ANIMALWHEELRADIUS, ANIMALWHEELWIDTH)
        geomWheel.setBody(wheel)    
        wheel.setPosition((wx + self.position[0], BASEHEIGHT + ANIMALWHEELRADIUS  + self.position[1], wz + self.position[2]))
        wheel.setRotation((cos(self.ang), 0, sin(self.ang), 0, 1, 0, -sin(self.ang), 0, cos(self.ang)))
        name = "AnimalWheel" + str(self.num)
        geomWheel.__setattr__('name', name)
        if self.viz and False:
            self.viz.addGeom(geomWheel)
            self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        return wheel, geomWheel

    def setLinearVelocity(self):
        self.rlJoint.setParam(ode.ParamFMax, 3)
        self.rrJoint.setParam(ode.ParamFMax, 3)
        self.rlJoint.setParam(ode.ParamVel, self.velocity/ANIMALWHEELRADIUS)
        self.rrJoint.setParam(ode.ParamVel, self.velocity/ANIMALWHEELRADIUS)

    def getPosition(self):
        return self.bodyAnimal.getPosition()

class Bridge(object):
    def __init__(self, world, space, viz, pos, sides):
        t, b = sides

        self.river = ode.GeomBox(space, (RIVERSIZE, 0.2, BASEWIDTH))
        self.river.setPosition((pos, BASEHEIGHT-1, 0.0))
        self.fxJoint = ode.FixedJoint(world)
        self.fxJoint.attach(self.river.getBody(), ode.environment)
        self.fxJoint.setFixed()
        self.sideWalk1 = ode.GeomBox(space, (RIVERSIZE + 2, 0.2, SIDEWALKSIZE))
        self.sideWalk1.setPosition((pos, BASEHEIGHT -.1, t + SIDEWALKSIZE/2))
        self.fxJoint1 = ode.FixedJoint(world)
        self.fxJoint1.attach(self.sideWalk1.getBody(), ode.environment)
        self.fxJoint1.setFixed()
        
        self.sideWalk2 = ode.GeomBox(space, (RIVERSIZE + 2, 0.2, SIDEWALKSIZE))
        self.sideWalk2.setPosition((pos, BASEHEIGHT -0.1, b - SIDEWALKSIZE/2))
        self.fxJoint2 = ode.FixedJoint(world)
        self.fxJoint2.attach(self.sideWalk2.getBody(), ode.environment)
        self.fxJoint2.setFixed()

        if viz:
          viz.addGeom(self.river)
          viz.addGeom(self.sideWalk1)
          viz.addGeom(self.sideWalk2)
          viz.GetProperty(self.river).SetColor(0, 0.5, 0.8)
          viz.GetProperty(self.sideWalk1).SetColor(0.349019608, 0.5, 0.450980392)
          viz.GetProperty(self.sideWalk2).SetColor(0.349019608, 0.5, 0.450980392)

        self.river.__setattr__('name','River')
        self.sideWalk1.__setattr__('name','Base')
        self.sideWalk2.__setattr__('name','Base')


class TreePole(object):
    def __init__(self, world, space, viz, position, tree, num):
        '''Position is a (x, 0, z) vector referenced from the car center'''
        self.world = world
        self.space = space
        self.viz = viz
        self.position = position 
        self.tree = tree
        if tree:
            self.color = TREECOLOR
            self.d = TREEDENSITY
        else:
            self.color = POLECOLOR
            self.d = POLEDENSITY
        self.num = num
        self.create()

    def create(self):
        self.geom = ode.GeomCylinder(self.space, TREEPOLERADIUS, TREEPOLEHEIGHT + BASEHEIGHT)
        x,y,z = self.position
        if (z < 0):
            ang =  pi
            self.geom.setRotation((cos(ang), -sin(ang), 0, 0, 0, -1, sin(ang), cos(ang), 0))
        else:
            self.geom.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))

        self.geom.setPosition((x, TREEPOLEHEIGHT/2 + 0.5 + BASEHEIGHT, z))
        self.fxJoint = ode.FixedJoint(self.world)
        self.fxJoint.attach(self.geom.getBody(), ode.environment)
        self.fxJoint.setFixed()
        if self.viz:
            self.viz.addGeom(self.geom)
            if (self.tree):
                self.viz.stlGeom(self.viz.GetObject(self.geom), TREEFILE)
            #self.viz.rotateActor(self.viz.GetObject(geom), np.array([1, 0, 0]), 180)
            else:
                self.viz.objGeom(self.viz.GetObject(self.geom), POLEFILE)
            self.viz.GetProperty(self.geom).SetColor(self.color)

        name = "TreePole" + str(self.num)
        self.geom.__setattr__('name', name)
    
    def getPosition(self):
        return self.geom.getPosition()

class Semaphore(object):
    def __init__(self, world, space, viz, position, status):
        '''Position is a (x, 0, z) vector referenced from the car center'''
        self.world = world
        self.space = space
        self.viz = viz
        self.position = position
        if status:
            self.colorRed = (51/255, 0, 0)
            self.colorGreen = (0, 1, 0)
        else:
            self.colorRed = (1, 0, 0)
            self.colorGreen = (0, 51/255, 0)
        self.create()

    def create(self):
        self.geomBase = ode.GeomCylinder(self.space, TREEPOLERADIUS/2, TREEPOLEHEIGHT + BASEHEIGHT)
        x,y,z = self.position
        self.geomBase.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.geomBase.setPosition((x, TREEPOLEHEIGHT/2 + 0.5 + BASEHEIGHT, z))
        self.fxJoint1 = ode.FixedJoint(self.world)
        self.fxJoint1.attach(self.geomBase.getBody(), ode.environment)
        self.fxJoint1.setFixed()
        self.geomBox = ode.GeomBox(self.space, (0.5, 0.9, 0.5))
        self.geomBox.setPosition((x, TREEPOLEHEIGHT + BASEHEIGHT + 1, z))
        self.fxJoint2 = ode.FixedJoint(self.world)
        self.fxJoint2.attach(self.geomBox.getBody(), ode.environment)
        self.fxJoint2.setFixed()
        self.green = ode.GeomCylinder(self.space, 0.2, 0.6)
        self.green.setRotation((0, 0, -1, 0, 1, 0, 1, 0, 0))
        self.green.setPosition((x, TREEPOLEHEIGHT + BASEHEIGHT + 0.8, z))
        self.fxJoint3 = ode.FixedJoint(self.world)
        self.fxJoint3.attach(self.green.getBody(), ode.environment)
        self.fxJoint3.setFixed()
        
        self.red = ode.GeomCylinder(self.space, 0.2, 0.6)
        self.red.setRotation((0, 0, -1, 0, 1, 0, 1, 0, 0))
        self.red.setPosition((x, TREEPOLEHEIGHT + BASEHEIGHT + 1.2, z))
        self.fxJoint4 = ode.FixedJoint(self.world)
        self.fxJoint4.attach(self.red.getBody(), ode.environment)
        self.fxJoint4.setFixed()
        if self.viz:
            self.viz.addGeom(self.geomBase)            
            self.viz.addGeom(self.geomBox)            
            self.viz.addGeom(self.green)
            self.viz.GetProperty(self.green).SetColor(self.colorGreen)
            self.viz.addGeom(self.red)
            self.viz.GetProperty(self.red).SetColor(self.colorRed)
        self.geomBase.__setattr__('name', 'Pole')
        self.geomBox.__setattr__('name', 'Box')
        self.red.__setattr__('name', 'Red')
        self.green.__setattr__('name', 'Green')
        allGroups.append([self.geomBase.getBody(), self.geomBox.getBody(), self.green.getBody(), self.red.getBody(), "Semaphore"])
