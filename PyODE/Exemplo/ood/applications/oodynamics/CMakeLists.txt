IF( WIN32 )
    ADD_DEFINITIONS( /wd4250 )
ENDIF( WIN32 )


SET(APPLICATION_NAME oodynamics )


ADD_EXECUTABLE(${APPLICATION_NAME} ${APPLICATION_NAME}.cpp)




IF( NOT DYNAMIC_OOD )


    TARGET_LINK_LIBRARIES(  ${APPLICATION_NAME}
                            osgdb_serializers_oodutil
                            osgdb_serializers_ood
    )


ENDIF( NOT DYNAMIC_OOD )


TARGET_LINK_LIBRARIES(  ${APPLICATION_NAME}
                        oodUtil
                        ood
                        osgDB
                        osg
)


IF(NOT WIN32)

    INSTALL(    TARGETS ${APPLICATION_NAME}
                RUNTIME DESTINATION bin)

ELSE(NOT WIN32)



    INSTALL(    TARGETS ${APPLICATION_NAME}
                RUNTIME DESTINATION bin
                LIBRARY DESTINATION lib
                ARCHIVE DESTINATION lib)



ENDIF(NOT WIN32)
