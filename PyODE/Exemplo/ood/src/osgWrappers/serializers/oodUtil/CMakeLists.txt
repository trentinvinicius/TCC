SET(MODULE_NAME osgdb_serializers_oodutil)
SET(LIBRARY_NAME oodUtil)




SET(TARGET_SRC
    AnimationHelper_serializer.cpp
    AnimationManager_serializer.cpp
    Curve_serializer.cpp
    HashTable_serializer.cpp
    HashTablePair_serializer.cpp
    LibraryWrapper.cpp
    Picker_serializer.cpp
)




IF( WIN32 )
    ADD_DEFINITIONS( "/wd4250" )
ENDIF( WIN32 )


SET(MODULE_LINK_LIBRARIES_WIN "osgDB osg OpenThreads opengl32 oodUtil")

OOD_SETUP_PLUGIN()
