SET(MODULE_NAME oodUtil)




SET(HEADER_PATH ${PROJECT_SOURCE_DIR}/include/${MODULE_NAME})




SET(TARGET_H
    ${HEADER_PATH}/AnimationHelper
    ${HEADER_PATH}/AnimationHelper.inl
    ${HEADER_PATH}/AnimationManager
    ${HEADER_PATH}/AnimationManager.inl
    ${HEADER_PATH}/ControllerBase
    ${HEADER_PATH}/ControllerBase.inl
    ${HEADER_PATH}/CPtr
    ${HEADER_PATH}/CreateTriMeshFromNode
    ${HEADER_PATH}/Curve
    ${HEADER_PATH}/Curve.inl
    ${HEADER_PATH}/FindObjects
    ${HEADER_PATH}/HashTable
    ${HEADER_PATH}/HashTable.inl
    ${HEADER_PATH}/Icosahedron
    ${HEADER_PATH}/Icosahedron.inl
    ${HEADER_PATH}/MatrixManipulator
    ${HEADER_PATH}/Picker
    ${HEADER_PATH}/Picker.inl
    ${HEADER_PATH}/Signal
    ${HEADER_PATH}/TrianglesEmitterIndexVisitor
    ${HEADER_PATH}/TrianglesEmitterIndexVisitor.inl
    ${HEADER_PATH}/TrianglesEmitterPrimitiveIndexFunctor
    ${HEADER_PATH}/TrianglesEmitterPrimitiveIndexFunctor.inl
    ${HEADER_PATH}/Version
)




SET(TARGET_SRC
    AnimationHelper.cpp
    AnimationManager.cpp
    ControllerBase.cpp
    CreateTriMeshFromNode.cpp
    Curve.cpp
    FindObjects.cpp
    HashTable.cpp
    Icosahedron.cpp
    MatrixManipulator.cpp
    Picker.cpp
    TrianglesEmitterIndexVisitor.cpp
    TrianglesEmitterPrimitiveIndexFunctor.cpp
    Version.cpp
)




SET( MODULE_LINK_LIBRARIES_GNU "ood osgGA osgDB osgUtil" )
SET( MODULE_LINK_LIBRARIES_WIN "ood osgAnimation osgGA osgDB osgUtil osg OpenThreads opengl32 ode" )

OOD_SETUP_LIBRARY()
