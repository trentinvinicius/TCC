import ode

allGroups = []

class Car(object):
    def __init__(self, world, space, viz): # adicionar numPassageiros e posicao e sentido(para outros carros)
        self.world = world
        self.space = space[0]
        self.viz = viz
        self.carLength = 3.0
        self.carWidth = 1.5
        self.carHeight = 0.1
        self.bodyCarColor = 0, 1.0, 0
        self.wheelLength = 0.15
        self.wheelRadius = 0.2
        self.wheelColor = 0, 0, 1.0
        self.create()

    def create(self):
        #create body
        self.bodyCar = ode.Body(self.world)
        mCar = ode.Mass()
        mCar.setBox(100, self.carLength, self.carHeight, self.carWidth)
        self.bodyCar.setMass(mCar)
        self.geomCar = ode.GeomBox(self.space, (self.carLength, self.carHeight, self.carWidth))
        self.geomCar.setBody(self.bodyCar)
        self.bodyCar.setPosition((0, self.wheelRadius, 0))
        self.viz.addGeom(self.geomCar)          
        self.viz.GetProperty(self.bodyCar).SetColor(self.bodyCarColor)
        #create wheels
        self.bodyFWL, self.geomFWL = self.createWheels( self.carLength/2 , -self.carWidth/2)
        self.bodyFWR, self.geomFWR = self.createWheels( self.carLength/2 ,  self.carWidth/2)
        self.bodyRWL, self.geomRWL = self.createWheels(-self.carLength/2 , -self.carWidth/2)
        self.bodyRWR, self.geomRWR = self.createWheels(-self.carLength/2 ,  self.carWidth/2)
        #create front left joint
        self.flJoint = ode.Hinge2Joint(self.world)
        self.flJoint.attach(self.bodyFWL, self.bodyCar)
        self.flJoint.setAnchor((self.carLength/2, self.wheelRadius, -self.carWidth/2))
        self.flJoint.setAxis1((0,0,1))
        self.flJoint.setAxis2((0,1,0))
        self.flJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.flJoint.setParam(ode.ParamSuspensionERP, 0.8)
        #create front right joint
        self.frJoint = ode.Hinge2Joint(self.world)
        self.frJoint.attach(self.bodyFWR, self.bodyCar)
        self.frJoint.setAnchor((self.carLength/2, self.wheelRadius, self.carWidth/2))
        self.frJoint.setAxis1((0,0,1))
        self.frJoint.setAxis2((0,1,0))
        self.frJoint.setParam(ode.ParamSuspensionCFM, 0.5)
        self.frJoint.setParam(ode.ParamSuspensionERP, 0.8)
        #create rear left joint
        self.rlJoint = ode.HingeJoint(self.world)
        self.rlJoint.attach(self.bodyRWL, self.bodyCar)
        self.rlJoint.setAnchor((-self.carLength/2, self.wheelRadius, -self.carWidth/2))
        self.rlJoint.setAxis((0,0,1))
        #create rear right joint
        self.rrJoint = ode.HingeJoint(self.world)
        self.rrJoint.attach(self.bodyRWR, self.bodyCar)
        self.rrJoint.setAnchor((-self.carLength/2, self.wheelRadius, self.carWidth/2))
        self.rrJoint.setAxis((0,0,1))
        # add Joints to allGroups
        allGroups.append([self.bodyFWL, self.bodyCar])
        allGroups.append([self.bodyFWR, self.bodyCar])
        allGroups.append([self.bodyRWL, self.bodyCar])
        allGroups.append([self.bodyRWR, self.bodyCar])
        #create front left motor
        self.flMotor = ode.AMotor(self.world)
        self.flMotor.attach(self.bodyRWL, self.bodyCar)
        self.flMotor.setNumAxes(1)
        self.flMotor.setAxis(0, 1, (0, 0, 1))
        self.flMotor.enable()      
        #create front right motor
        self.frMotor = ode.AMotor(self.world)
        self.frMotor.attach(self.bodyRWR, self.bodyCar)
        self.frMotor.setNumAxes(1)
        self.frMotor.setAxis(0, 1, (0, 0, 1))
        self.frMotor.enable()

    def createWheels(self, wx, wz):
        wheel = ode.Body(self.world)
        mWheel = ode.Mass()
        mWheel.setCylinder(100, 3, self.wheelRadius, self.wheelLength) #density, direction(1,2,3), r, h
        wheel.setMass(mWheel)
        geomWheel = ode.GeomCylinder(self.space, self.wheelRadius, self.wheelLength)
        geomWheel.setBody(wheel)
        wheel.setPosition((wx, self.wheelRadius, wz))
        self.viz.addGeom(geomWheel)
        self.viz.GetProperty(wheel).SetColor(self.wheelColor)
        return wheel, geomWheel

    def setLinearVelocity(self, velocity):
        vx, vy, vz = velocity
        self.bodyCar.setLinearVel((vx, vy, vz))

    def addTorque(self, torque):
        '''self.flJoint.setParam(ode.ParamVel, 10)
        self.frJoint.setParam(ode.ParamVel, 10)
        self.flJoint.setParam(ode.ParamVel2, 100)
        self.frJoint.setParam(ode.ParamVel2, 100)
        #self.flJoint.setParam(ode.ParamFMax, 10)
        self.flMotor.addTorques(torque, 0.0, 0.0)
        self.frMotor.addTorques(torque, 0.0, 0.0)'''
        #self.flJoint.addTorques(torque, torque)
        #self.frJoint.addTorques(torque, torque)
        '''
        self.rlJoint.addTorque(torque)
        self.rrJoint.addTorque(torque)'''
        self.rlJoint.setParam(ode.ParamVel, 30)
        self.rrJoint.setParam(ode.ParamVel, 30)
        self.rlJoint.setParam(ode.ParamVel2, 30)
        self.rrJoint.setParam(ode.ParamVel2, 30)

    def steer(self, ang):
        pass

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
