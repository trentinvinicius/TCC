SET(MODULE_NAME osgdb_serializers_ood)
SET(LIBRARY_NAME ood)




SET(TARGET_SRC
    AMotorJoint_serializer.cpp
    AerodynamicDevice_serializer.cpp
    AutoRemoveUpdateCallback_serializer.cpp
    BallJoint_serializer.cpp
    Box_serializer.cpp
    BypassJoint_serializer.cpp
    Calendar_serializer.cpp
    Capsule_serializer.cpp
    CharacterBase_serializer.cpp
    Character_serializer.cpp
    Collidable_serializer.cpp
    CollisionCallback_serializer.cpp
    CollisionParameters_serializer.cpp
    Container_serializer.cpp
    CubicVec3Interpolator_serializer.cpp
    Cylinder_serializer.cpp
    DBallJoint_serializer.cpp
    DHingeJoint_serializer.cpp
    DefaultNearCallback_serializer.cpp
    DifferentialJoint_serializer.cpp
    EngineBase_serializer.cpp
    Engine_serializer.cpp
    Events_serializer.cpp
    FixedJoint_serializer.cpp
    GearboxJoint_serializer.cpp
    Generic6DofJoint_serializer.cpp
    Hinge2Joint_serializer.cpp
    HingeJoint_serializer.cpp
    InterpolatorBase_serializer.cpp
    JointBreakCallback_serializer.cpp
    JointServoMotor_serializer.cpp
    Joint_serializer.cpp
    LMPlusJoint_serializer.cpp
    LMotorJoint_serializer.cpp
    LibraryWrapper.cpp
    LinearInterpolator_serializer.cpp
    LinearQuatInterpolator_serializer.cpp
    LinearVec3Interpolator_serializer.cpp
    ManagerEventHandler_serializer.cpp
    ManagerUpdateCallback_serializer.cpp
    Manager_serializer.cpp
    MotionPath_serializer.cpp
    MotorJoint_serializer.cpp
    NearCallback_serializer.cpp
    ODECallback_serializer.cpp
    ODEObject_serializer.cpp
    PIDController_serializer.cpp
    PistonJoint_serializer.cpp
    Plane2DJoint_serializer.cpp
    QuatInterpolator_serializer.cpp
    RagDoll_serializer.cpp
    RayCar_serializer.cpp
    RayWheel_serializer.cpp
    RigidBodyServoMotor_serializer.cpp
    RigidBody_serializer.cpp
    ScalarInterpolator_serializer.cpp
    ServoMotor_serializer.cpp
    SliderJoint_serializer.cpp
    Space_serializer.cpp
    Sphere_serializer.cpp
    SuspensionJoint_serializer.cpp
    SwaybarJoint_serializer.cpp
    ThreadedManagerUpdateCallback_serializer.cpp
    ThreadedManager_serializer.cpp
    Transformable_serializer.cpp
    TriMesh_serializer.cpp
    UniversalJoint_serializer.cpp
    Vec3Interpolator_serializer.cpp
    Wheel_serializer.cpp
    World_serializer.cpp
)




SET(MODULE_LINK_LIBRARIES_WIN "ood osgGA osgAnimation osgDB osg OpenThreads opengl32 ode")

OOD_SETUP_PLUGIN()
