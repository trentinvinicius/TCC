' some globals'
Dim shared as dWorldID      world
dim shared as dSpaceID      world_space
dim shared as dGeomID       geomground,geombox,geombox2, gWheel1, gWheel2,gWheel3,gWheel4, gChassis,gRollbar, gRamp,gMotor
dim shared as dBodyID       bodybox, tractorbox,tbox2, bWheel1,bWheel2,bWheel3, bWheel4,bChassis,bRollbar,bRamp,bMotor
dim shared as dJointGroupID contactgroup
dim shared as dContact      contacts(MAX_CONTACTS-1)
dim shared as dJointID      hing
dim shared as integer draw_contacts = 1

Dim As Single ts1=3f,ts2=2f,ts3=7.3f
Dim as dMass m,m2
Dim As dJointID jWheel1, jWheel2,jWheel3, jWheel4,jRollbar,jRamp,jMotor
   
   dInitODE2(0)
' create world and set gravity'
   world = dWorldCreate()
   dWorldSetGravity(world,0,GRAVITY,0)
' craete a contact group (faster to delete)'
   contactgroup = dJointGroupCreate(0)
 create an space for our objects
   world_space = dHashSpaceCreate(0)
' the ground are an static object (geom only)'
   geomground = dCreatePlane(world_space,0,1,0,0)
   
' the box are an dynamic object (body and geom)'
   dWorldSetAutoDisableFlag(World,1)
   dWorldSetERP(World,1)

'CREATE CAR (PHYSICS BODIES) '  
   bwheel1 = dBodyCreate(world)
   bwheel2 = dBodyCreate(world)
   bwheel3 = dBodyCreate(world)
   bwheel4 = dBodyCreate(world)
   bchassis = dBodyCreate(world)
   bMotor = dBodyCreate(world)
'CALCULATE MASS FOR CAR PARTS (PHYSICS BODIES) '  
   dMassSetSphereTotal(@m,14,0.7) '14 , 50'
   dMassSetBoxTotal(@m2,200,SIDEa,SIDEb,SIDEc)
   dMassTranslate(@m,0,0,0)
   
'BIND MASS TO CAR PARTS (PHYSICS BODIES)   2'

   dBodySetMass (bwheel1,@m)
   dBodySetMass (bwheel2,@m)
   dBodySetMass (bwheel3,@m)
   dBodySetMass (bwheel4,@m)
   dBodySetMass (bchassis,@m2)

   dBodySetMass (bmotor,@m)
   
   Dim As Single cary = 1.1
      
'POSITION CAR PARTS (PHYSICS BODIES)  ' 
   dBodySetPosition  (bwheel1,-2,cary-0.5,+3)
   dBodySetPosition  (bwheel2,+2,cary-0.5,+3)
   dBodySetPosition  (bwheel3,-2,cary-0.5,-3)
   dBodySetPosition  (bwheel4,+2,cary-0.5,-3)
   dBodySetPosition  (bchassis,0,cary,0) 
   dBodySetPosition  (bchassis,0,1,0)
   
   dBodySetPosition  (brollbar,0,2.3,0.01) 'Y=2 default'
   dBodySetPosition  (bmotor,0,2.3,-3) 'Y=2 default'
   
'CREATE GEOMETRY FOR CAR PARTS (GEOMETRIC BODIES)   '
   gWheel1 = dCreateSphere(world_space,0.7)
   gWheel2 = dCreateSphere(world_space,0.7)
   gWheel3 = dCreateSphere(world_space,0.7)
   gWheel4 = dCreateSphere(world_space,0.7)
   gChassis = dCreateBox(world_space,SIDEa,SIDEb,SIDEc)

   gRollbar = dCreateSphere(world_space,0.8)
   gMotor = dCreateSphere(world_space,0.2)
'BIND GEOMETRY TO CAR PARTS (PHYSICS BODIES)   '
   dGeomSetBody (gWheel1,bWheel1)
   dGeomSetBody (gWheel2,bWheel2)
   dGeomSetBody (gWheel3,bWheel3)
   dGeomSetBody (gWheel4,bWheel4)
   dGeomSetBody (gChassis,bChassis)

   dGeomSetBody (gMotor,bMotor)
   
'CREATE JOINTS (PHYSICS BODIES) '  
   jWheel1 = dJointCreateHinge2 (World,0)   
   jWheel2 = dJointCreateHinge2 (World,0)
   jWheel3 = dJointCreateHinge2 (World,0)   
   jWheel4 = dJointCreateHinge2 (World,0)
   
   jMotor = dJointCreateSlider(World,0)

'BIND CAR PARTS TOGETHER WITH JOINTS (PHYSICS BODIES)   '
   dJointAttach (jWheel1, bChassis, bWheel1)
   dJointAttach (jWheel2, bChassis, bWheel2)
   dJointAttach (jWheel3, bChassis, bWHeel3)
   dJointAttach (jWheel4, bChassis, bWheel4)

   dJointAttach (jMotor, bChassis, bMotor)
   
'SET JOINT PARAMATERS (PHYSICS BODIES)'

        Dim as dReal Ptr a
        a = dBodyGetPosition(bWheel1)
        dJointSetHinge2Anchor(jWheel1,a[0],a[1],a[2])
        a = dBodyGetPosition(bWheel2)
        dJointSetHinge2Anchor(jWheel2,a[0],a[1],a[2])
        a = dBodyGetPosition(bWheel3)
        dJointSetHinge2Anchor(jWheel3,a[0],a[1],a[2])
        a = dBodyGetPosition(bWheel4)
        dJointSetHinge2Anchor(jWheel4,a[0],a[1],a[2])


   dJointSetSliderParam (jMotor,dParamLoStop,-1)
   dJointSetSliderParam (jMotor,dParamHiStop,1)


   dJointSetHinge2Param (jWheel3,dParamLoStop,0)
   dJointSetHinge2Param (jWheel3,dParamHiStop,0)
   dJointSetHinge2Param (jWheel4,dParamLoStop,0)
   dJointSetHinge2Param (jWHeel4,dParamHiStop,0)
   
   
   dJointSetHinge2Axis1 (jWheel1,   0,   1,   0)
   dJointSetHinge2Axis2 (jWheel1,   -1,   0,   0)
   dJointSetHinge2Param(jWheel1,dParamSuspensionERP,1)
   dJointSetHinge2Param(jWheel1,dParamSuspensionCFM,0.001)

   
   dJointSetHinge2Axis1 (jWheel2,   0,   1,   0)
   dJointSetHinge2Axis2 (jWheel2,   -1,   0,   0)
   dJointSetHinge2Param(jWheel2,dParamSuspensionERP,1)
   dJointSetHinge2Param(jWheel2,dParamSuspensionCFM,0.001)
   
   
   
   dJointSetHinge2Axis1 (jWheel3,   0,   1,   0)
   dJointSetHinge2Axis2 (jWheel3,   -1,   0,   0)
   dJointSetHinge2Param(jWheel3,dParamSuspensionERP,1)
   dJointSetHinge2Param(jWheel3,dParamSuspensionCFM,0.003)


   
   dJointSetHinge2Axis1 (jWheel4,   0,   1,   0)
   dJointSetHinge2Axis2 (jWheel4,   -1,   0,   0)
   dJointSetHinge2Param(jWheel4,dParamSuspensionERP,1)
   dJointSetHinge2Param(jWheel4,dParamSuspensionCFM,0.003)
   
      
   dJointSetHinge2Param (jWheel1,dParamVel2,0)
   dJointSetHinge2Param (jWheel2,dParamVel2,0)
   dJointSetHinge2Param (jWheel3,dParamVel2,0)
   dJointSetHinge2Param (jWheel4,dParamVel2,0)     