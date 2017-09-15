# Install script for directory: /home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/src/oodUtil

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/oodUtil" TYPE FILE FILES
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/AnimationHelper"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/AnimationHelper.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/AnimationManager"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/AnimationManager.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/ControllerBase"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/ControllerBase.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/CPtr"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/CreateTriMeshFromNode"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Curve"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Curve.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/FindObjects"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/HashTable"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/HashTable.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Icosahedron"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Icosahedron.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/MatrixManipulator"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Picker"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Picker.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Signal"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/TrianglesEmitterIndexVisitor"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/TrianglesEmitterIndexVisitor.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/TrianglesEmitterPrimitiveIndexFunctor"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/TrianglesEmitterPrimitiveIndexFunctor.inl"
    "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/include/oodUtil/Version"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib64" TYPE SHARED_LIBRARY FILES "/home/vinicius/Dropbox/TCCViniciusTrentin/TCC/PyODE/Exemplo/ood/build/src/oodUtil/liboodUtil.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/liboodUtil.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/liboodUtil.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib64/liboodUtil.so")
    endif()
  endif()
endif()

