# Install script for directory: /home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/src/ood

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ood" TYPE FILE FILES
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/AMotorJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/AMotorJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/AerodynamicDevice"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/AerodynamicDevice.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/AutoRemoveUpdateCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/AutoRemoveUpdateCallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/BallJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Box"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/BypassJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/BypassJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Calendar"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Calendar.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Capsule"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Character"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CharacterBase"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CharacterBase.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Collidable"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Collidable.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CollisionCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CollisionCallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CollisionParameters"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CollisionParameters.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CommonRayCastResults"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CommonRayCastResults.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CommonWorldOperations"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Config"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Container"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Container.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/CubicVec3Interpolator"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Cylinder"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/DBallJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/DHingeJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/DefaultNearCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/DefaultNearCallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/DifferentialJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/DifferentialJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Engine"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Engine.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/EngineBase"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/EngineBase.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Events"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Events.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Export"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/FixedJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/FixedJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/GearboxJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/GearboxJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Generic6DofJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Generic6DofJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Hinge2Joint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Hinge2Joint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/HingeJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/HingeJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Interpolator"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Joint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Joint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/JointBreakCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/JointBreakCallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/JointFeedback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/JointFeedback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/JointServoMotor"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/JointServoMotor.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/LMPlusJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/LMotorJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/LMotorJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/LinearInterpolator"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/LinearQuatInterpolator"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/LinearVec3Interpolator"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Manager"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Manager.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ManagerEventHandler"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ManagerEventHandler.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ManagerUpdateCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ManagerUpdateCallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/MotionPath"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/MotionPath.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/MotorJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/MotorJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/NearCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Notify"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Notify_android"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Notify_gnu"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Notify_windows"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/OCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ODE"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ODECallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ODECallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ODEObject"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ODEObject.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/OObject"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/OverlappingPair"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/OverlappingPair.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/PIDController"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/PIDController.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/PistonJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/PistonJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Plane2DJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Plane2DJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RagDoll"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RagDoll.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RayCar"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RayCar.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RayWheel"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RayWheel.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RigidBody"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RigidBody.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RigidBodyServoMotor"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/RigidBodyServoMotor.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ScopedTimer"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ScopedTimer.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ServoMotor"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ServoMotor.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/SliderJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/SliderJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Space"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Space.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Sphere"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/StaticWorld"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/StaticWorld.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/SuspensionJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/SuspensionJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/SwaybarJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/SwaybarJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ThreadedManager"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ThreadedManager.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ThreadedManagerUpdateCallback"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/ThreadedManagerUpdateCallback.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Transformable"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Transformable.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/TriMesh"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/TriMesh.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/UniversalJoint"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/UniversalJoint.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Version"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Wheel"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/Wheel.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/World"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/ood/World.inl"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/libood.so.2.3.0"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/libood.so.41"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/libood.so"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib64" TYPE SHARED_LIBRARY FILES
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/build/src/ood/libood.so.2.3.0"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/build/src/ood/libood.so.41"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/build/src/ood/libood.so"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/libood.so.2.3.0"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/libood.so.41"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/libood.so"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHANGE
           FILE "${file}"
           OLD_RPATH "/usr/local/lib:"
           NEW_RPATH "")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

