IF( WIN32 )
    SET(TARGET_DEFAULT_PREFIX "example_")
ELSE( WIN32 )
    SET(TARGET_DEFAULT_PREFIX "")
ENDIF( WIN32 )

SET(TARGET_DEFAULT_LABEL_PREFIX "Examples")



SET(TARGET_COMMON_LIBRARIES
    OpenThreads
    osg
    osgDB
    osgUtil
    osgGA
    osgViewer
    ood
    oodUtil
)


IF( WIN32 )
    ADD_DEFINITIONS( /wd4250 )
ENDIF( WIN32 )

ADD_DEFINITIONS( -DOOD_DATA_PATH="${OOD_SAMPLE_DATA}" )




ADD_SUBDIRECTORY( oodaerodynamicdevice )
ADD_SUBDIRECTORY( oodamotor )
ADD_SUBDIRECTORY( oodamotorstop )
# ADD_SUBDIRECTORY( oodandroidgles1 )
ADD_SUBDIRECTORY( oodbox )
ADD_SUBDIRECTORY( oodcapsule )

IF( OOD_BUILD_OOS_EXAMPLES )
    ADD_SUBDIRECTORY( oodcar )
ENDIF( OOD_BUILD_OOS_EXAMPLES )

ADD_SUBDIRECTORY( oodcharacter )

IF( OOD_BUILD_OOS_EXAMPLES )
    ADD_SUBDIRECTORY( oodcollisionsound )
ENDIF( OOD_BUILD_OOS_EXAMPLES )

ADD_SUBDIRECTORY( ooddhingejoint )
ADD_SUBDIRECTORY( ooddifferentialjoint )
ADD_SUBDIRECTORY( oodengine )
ADD_SUBDIRECTORY( oodgearboxjoint )
ADD_SUBDIRECTORY( oodhingejoint )
ADD_SUBDIRECTORY( oodlmotor )
ADD_SUBDIRECTORY( oodlmplusjoint )
ADD_SUBDIRECTORY( oodpendulum )
ADD_SUBDIRECTORY( oodplane2djoint )
ADD_SUBDIRECTORY( oodrigidbody )
ADD_SUBDIRECTORY( oodrope )
ADD_SUBDIRECTORY( oodsliderjoint )
ADD_SUBDIRECTORY( oodspacestress )
ADD_SUBDIRECTORY( oodtrimesh )
ADD_SUBDIRECTORY( ooduniversaljoint )
ADD_SUBDIRECTORY( oodutilcontrollerbase )
ADD_SUBDIRECTORY( oodutilpicker )
