import ode
import numpy as np
from math import cos, sin, pi, atan2, sqrt
from constants import *

allGroups = []
bodies = []
bodiesNames = []

'''

Fazer metodo de parametrizacao
parametrizar situacao como AG para facilitar criacao de situaceos dificeis
'''

'''Consideraceos:

outros veiculos e pessoas nao mudam velocidade nem direcao
uma vez tomada a decisao ele nao sera mudada (referindo-se a generalizacao por nn)
'''

class Car(object):
    def __init__(self, world, space, viz, dist, passengers = 5, mainCar = True, position = (0.0, 0.0, 0.0), direction = 1):
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.passengers = passengers
        self.direction = direction
        if self.direction == 1:
            self.position = np.array(position) - np.array((dist, 0, 0))
        else:
            self.position = np.array(position) + np.array((dist, 0, 0))
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
        self.bodyCar.setPosition((0 + self.position[0], BASEHEIGHT + WHEELRADIUS + CARHEIGHT/2 + self.position[1], 0 + self.position[2]))
        self.viz.addGeom(self.geomCar)          
        self.viz.GetProperty(self.bodyCar).SetColor(self.bodyCarColor)
        #create wheels
        if (self.direction == -1):
           self.bodyFWL, self.geomFWL = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyFWR, self.geomFWR = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
           self.bodyRWL, self.geomRWL = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyRWR, self.geomRWR = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
           self.viz.stlGeom(self.viz.GetObject(self.geomCar), CARCOMINGFILE)
        else: #if (self.direction == 1):
           self.bodyFWL, self.geomFWL = self.createWheels( CARLENGTH/2 , -CARWIDTH/2)
           self.bodyFWR, self.geomFWR = self.createWheels( CARLENGTH/2 ,  CARWIDTH/2)
           self.bodyRWL, self.geomRWL = self.createWheels(-CARLENGTH/2 , -CARWIDTH/2)
           self.bodyRWR, self.geomRWR = self.createWheels(-CARLENGTH/2 ,  CARWIDTH/2)
           self.viz.stlGeom(self.viz.GetObject(self.geomCar), CARGOINGFILE)
        #create front left joint
        '''self.flJoint = ode.Hinge2Joint(self.world)
        self.flJoint.attach(self.bodyCar, self.bodyFWL)
        if (self.direction == 1):
           self.flJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        else:
           self.flJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.flJoint.setAxis2((0,0,1))
        self.flJoint.setAxis1((0,1,0))
        self.flJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJoint.setParam(ode.ParamSuspensionERP, 0.8)'''
        self.flJointRoll = ode.HingeJoint(self.world)
        self.flJointYaw  = ode.HingeJoint(self.world)
        flJointBody = ode.Body(self.world)
        nullMass1 = ode.Mass()
        nullMass1.setBox(0.01, 0.01, 0.01, 0.01)
        flJointBody.setMass(nullMass1)
        self.flJointRoll.attach(flJointBody, self.bodyFWL)
        self.flJointYaw.attach(self.bodyCar, flJointBody)
        if (self.direction == 1):
           flJointBody.setPosition((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
           self.flJointRoll.setAnchor((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
           self.flJointYaw.setAnchor((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        else:
           flJointBody.setPosition((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
           self.flJointRoll.setAnchor((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
           self.flJointYaw.setAnchor((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.flJointRoll.setAxis((0,0,1))
        self.flJointYaw.setAxis((0,1,0))
        self.flJointRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJointRoll.setParam(ode.ParamSuspensionERP, 0.8)
        self.flJointYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJointYaw.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right joint
        '''self.frJoint = ode.Hinge2Joint(self.world)
        self.frJoint.attach(self.bodyCar, self.bodyFWR)
        if (self.direction == 1):
           self.frJoint.setAnchor((CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        else:
           self.frJoint.setAnchor((-CARLENGTH/2 + self.position[0], WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        self.frJoint.setAxis2((0,0,1))
        self.frJoint.setAxis1((0,1,0))
        self.frJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJoint.setParam(ode.ParamSuspensionERP, 0.8)'''
        self.frJointRoll = ode.HingeJoint(self.world)
        self.frJointYaw  = ode.HingeJoint(self.world)
        frJointBody = ode.Body(self.world)
        nullMass2 = ode.Mass()
        nullMass2.setBox(0.01, 0.01, 0.01, 0.01)
        frJointBody.setMass(nullMass2)
        self.frJointRoll.attach(frJointBody, self.bodyFWR)
        self.frJointYaw.attach(self.bodyCar, frJointBody)
        if (self.direction == 1):
           frJointBody.setPosition((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
           self.frJointRoll.setAnchor((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
           self.frJointYaw.setAnchor((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        else:
           frJointBody.setPosition((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
           self.frJointRoll.setAnchor((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
           self.frJointYaw.setAnchor((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], - CARWIDTH/2 + self.position[2]))
        self.frJointRoll.setAxis((0,0,1))
        self.frJointYaw.setAxis((0,1,0))
        self.frJointRoll.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJointRoll.setParam(ode.ParamSuspensionERP, 0.8)
        self.frJointYaw.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJointYaw.setParam(ode.ParamSuspensionERP, 0.8)
        #create rear left joint
        self.rlJoint = ode.HingeJoint(self.world)
        self.rlJoint.attach(self.bodyCar, self.bodyRWL)
        if (self.direction == 1):
           self.rlJoint.setAnchor((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], -CARWIDTH/2 + self.position[2]))
        else:
           self.rlJoint.setAnchor((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        self.rlJoint.setAxis((0,0,1))
        #create rear right joint
        self.rrJoint = ode.HingeJoint(self.world)
        self.rrJoint.attach(self.bodyCar, self.bodyRWR)
        if (self.direction == 1):
           self.rrJoint.setAnchor((-CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], CARWIDTH/2 + self.position[2]))
        else:
           self.rrJoint.setAnchor((CARLENGTH/2 + self.position[0], BASEHEIGHT + WHEELRADIUS + self.position[1], -CARWIDTH/2 + self.position[2]))
        self.rrJoint.setAxis((0,0,1))
        # add Joints to allGroups
        '''allGroups.append([self.bodyFWL, self.bodyCar])
        allGroups.append([self.bodyFWR, self.bodyCar])
        allGroups.append([self.bodyRWL, self.bodyCar])
        allGroups.append([self.bodyRWR, self.bodyCar])'''
        allGroups.append([self.bodyFWL, self.bodyFWR, self.bodyRWL, self.bodyRWR, nullMass2, nullMass1, self.bodyCar])

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

    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinderTotal(WHEELWEIGHT, 3, WHEELRADIUS, WHEELWIDTH) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, WHEELRADIUS, WHEELWIDTH)
        geomWheel.setBody(wheel)    
    
        wheel.setPosition((wx + self.position[0], BASEHEIGHT + WHEELRADIUS  + self.position[1], wz + self.position[2]))
        self.viz.addGeom(geomWheel)
        self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        return wheel, geomWheel

    def setLinearVelocity(self, velocity):
        vx = (self.direction*velocity)/WHEELRADIUS
        #self.bodyCar.setLinearVel((vx, 0, 0))
        self.flMotorRoll.setParam(ode.ParamFMax, 10000)
        self.frMotorRoll.setParam(ode.ParamFMax, 10000)
        self.rlMotorRoll.setParam(ode.ParamFMax, 10000)
        self.rrMotorRoll.setParam(ode.ParamFMax, 10000)
        
        self.flMotorRoll.setParam(ode.ParamVel, vx)
        self.frMotorRoll.setParam(ode.ParamVel, vx)
        self.rlMotorRoll.setParam(ode.ParamVel, vx)
        self.rrMotorRoll.setParam(ode.ParamVel, vx)

    def getLinearVelocity(self):
        return self.bodyCar.getLinearVel()[0]
        
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

    def inPosition(self):
        aux = self.getPosition()[0]
        if (aux > 0 and int(aux) == 0):
            return True
        return False

    def brake(self):
        self.flMotorRoll.setParam(ode.ParamFMax, 0)
        self.frMotorRoll.setParam(ode.ParamFMax, 0)
        self.rlMotorRoll.setParam(ode.ParamFMax, 0)
        self.rrMotorRoll.setParam(ode.ParamFMax, 0)

        rBrakeForce = 250.0
        fBrakeForce = 500.0
        self.flJointRoll.setParam(ode.ParamVel, 0.0)
        self.flJointRoll.setParam(ode.ParamFMax, fBrakeForce)
        self.frJointRoll.setParam(ode.ParamVel, 0.0)
        self.frJointRoll.setParam(ode.ParamFMax, fBrakeForce)
        self.rlJoint.setParam(ode.ParamVel, 0.0)
        self.rlJoint.setParam(ode.ParamFMax, rBrakeForce)
        self.rrJoint.setParam(ode.ParamVel, 0.0)
        self.rrJoint.setParam(ode.ParamFMax, rBrakeForce)

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
        self.yPos =  0.20834342658224672 - WHEELRADIUS + ROADHEIGHT + BASEHEIGHT
        self.create()

    def create(self):
        #self.body = ode.Body(self.world)
        #mass = ode.Mass()
        #mass.setBox(ROADDENSITY, ROADLENGTH, ROADHEIGHT, self.size)
        #self.body.setMass(mass)
        self.geom = ode.GeomBox(self.space, (ROADLENGTH, ROADHEIGHT, self.size))
        #self.geom.setBody(self.body)
        self.geom.setPosition((ROADLENGTH/2 - 100.0 , BASEHEIGHT, self.zPos))
        self.viz.addGeom(self.geom)
        #self.viz.GetProperty(self.body).SetColor(ROADCOLOR)
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
    def __init__(self, world, space, viz, position, velocity):
        '''Position is a (x, 0, z) vector referenced from the car center
           Velocity is a three component vector (vx, 0, vz)'''
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.position = position
        self.velocity = velocity
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        mass = ode.Mass()
        mass.setCylinderTotal(75, 2, PERSONRADIUS, PERSONHEIGHT)
        geom = ode.GeomCylinder(self.space, PERSONRADIUS, PERSONHEIGHT)
        geom.setBody(self.body)
        x,y,z = self.position
        self.body.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.body.setPosition((x, BASEHEIGHT + y + PERSONHEIGHT/2 + SPHERERADIUS, z))
        self.viz.addGeom(geom)
        self.viz.GetProperty(self.body).SetColor(PERSONCOLOR)
        self.viz.stlGeom(self.viz.GetObject(geom), PERSONFILE)
        
        #create spheres
        self.w1, gw1 = self.createSphere(x + PERSONRADIUS - SPHERERADIUS, z)
        self.w2, gw2 = self.createSphere(x - PERSONRADIUS + SPHERERADIUS, z)
        self.w3, gw3 = self.createSphere(x, z - PERSONRADIUS + SPHERERADIUS)

        #create joints
        self.j1 = ode.BallJoint(self.world)
        self.j1.attach(self.w1, self.body)
        self.j1.setAnchor((x + PERSONRADIUS - SPHERERADIUS, BASEHEIGHT + SPHERERADIUS, z))
        self.j2 = ode.BallJoint(self.world)
        self.j2.attach(self.w2, self.body)
        self.j2.setAnchor((x - PERSONRADIUS + SPHERERADIUS, BASEHEIGHT + SPHERERADIUS, z))
        self.j3 = ode.BallJoint(self.world)
        self.j3.attach(self.w3, self.body)
        self.j3.setAnchor((x, BASEHEIGHT + SPHERERADIUS, z - PERSONRADIUS + SPHERERADIUS))
   
        #add body and wheels to allGroups
        allGroups.append([self.w1, self.body])
        allGroups.append([self.w2, self.body])
        allGroups.append([self.w3, self.body])
       
        #self.setLinearVelocity()
        
    def createSphere(self, sx, sz):
        sphere = ode.Body(self.world)
        mSphere = ode.Mass()
        mSphere.setSphere(PERSONDENSITY, SPHERERADIUS)
        sphere.setMass(mSphere)
        geomSphere = ode.GeomSphere(self.space, SPHERERADIUS)
        geomSphere.setBody(sphere)    
        sphere.setPosition((sx, BASEHEIGHT + SPHERERADIUS, sz))
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
        wheel.setPosition((wx, BASEHEIGHT + SPHERERADIUS, wz))
        self.viz.addGeom(geomWheel)
        self.viz.GetProperty(wheel).SetColor(WHEELCOLOR)
        return wheel, geomWheel

    def setLinearVelocity(self):
        vx, vy, vz = self.velocity
        self.w1.setLinearVel((vx, vy, vz))
        self.w2.setLinearVel((vx, vy, vz))
        self.w3.setLinearVel((vx, vy, vz))


class TreePole(object):
    def __init__(self, world, space, viz, position, tree, base):
        '''Position is a (x, 0, z) vector referenced from the car center'''
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.position = position
        self.tree = tree
        if tree:
            self.color = TREECOLOR
            self.d = TREEDENSITY
        else:
            self.color = POLECOLOR
            self.d = POLEDENSITY
        self.base = base
        self.create()

    def create(self):
        self.body = ode.Body(self.world)
        '''
        base = ode.Body(self.world)
        baseMass = ode.Mass()
        baseMass.setBoxTotal(1000000.0, 1.0, 0.02, 1.0)
        base.setMass(baseMass)
        geomBase = ode.GeomBox(self.space, (1.0, 0.02, 1.0))
        geomBase.setBody(base)
        '''
        mass = ode.Mass()
        mass.setCylinder(1*self.d, 2, TREEPOLERADIUS, TREEPOLEHEIGHT + BASEHEIGHT)
        self.body.setMass(mass)
        geom = ode.GeomCylinder(self.space, TREEPOLERADIUS, TREEPOLEHEIGHT + BASEHEIGHT)
        geom.setBody(self.body)
        x,y,z = self.position
        geom.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        geom.setPosition((x, TREEPOLEHEIGHT/2 + 1 + BASEHEIGHT, z))
        #geom.setBody(self.base)

        '''self.base2 = ode.Body(self.world)
        mass2 = ode.Mass()
        mass2.setCylinder(5*self.d, 2, 1.0, BASEHEIGHT)
        self.base2.setMass(mass2)
        geom2 = ode.GeomCylinder(self.space, 1.0, BASEHEIGHT)
        geom2.setBody(self.base2)
        self.base2.setRotation((1, 0, 0, 0, 0, -1, 0, 1, 0))
        self.base2.setPosition((x, BASEHEIGHT/2, z))'''

        #allGroups.append((self.base, self.base2))
        #allGroups.append((self.base2, self.body))
        fxJoint = ode.FixedJoint(self.world)
        fxJoint.attach(self.body, ode.environment)
        fxJoint.setFixed()
        #fxJoint.setAnchor((x, BASEHEIGHT/2, z))
        #fxJoint.setAxis((0,1,0))
        #base.setPosition((x, y, z))
        self.viz.addGeom(geom)
        #self.viz.addGeom(geom2)
        #self.viz.addGeom(geomBase)
        #j = ode.FixedJoint(self.world)
        #j.attach(self.body, ode.environment)
        if (self.tree):
            pass
            self.viz.stlGeom(self.viz.GetObject(geom), TREEFILE)
            #self.viz.rotateActor(self.viz.GetObject(geom), np.array([1, 0, 0]), 180)
        #self.viz.GetProperty(self.body).SetColor(self.color)