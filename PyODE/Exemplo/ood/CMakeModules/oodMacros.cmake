MACRO(OOD_SETUP_LIBRARY)


    IF( WIN32 )
        SOURCE_GROUP(Headers FILES ${TARGET_H})
    ENDIF( WIN32 )




    INSTALL(    FILES ${TARGET_H}
                DESTINATION include/${MODULE_NAME}
    )




    ADD_LIBRARY(    ${MODULE_NAME}
                    ${OOD_USER_DEFINED_DYNAMIC_OR_STATIC}
                    ${TARGET_SRC}
                    ${TARGET_H}
    )




    SET_TARGET_PROPERTIES(  ${MODULE_NAME}
                            PROPERTIES
                            VERSION ${OOD_VERSION}
                            SOVERSION ${OOD_SOVERSION}
    )








    IF( WIN32 )

        SET(MODULE_LINK_LIBRARIES ${MODULE_LINK_LIBRARIES_WIN})


    ELSE( WIN32 )

        SET(MODULE_LINK_LIBRARIES ${MODULE_LINK_LIBRARIES_GNU})

    ENDIF( WIN32 )




    STRING(REGEX REPLACE " " ";" MODULE_LINK_LIBRARIES ${MODULE_LINK_LIBRARIES})



    TARGET_LINK_LIBRARIES(  ${MODULE_NAME}
                            ${MODULE_LINK_LIBRARIES}
    )




    MESSAGE(STATUS "${MODULE_NAME} link libraries: ${MODULE_LINK_LIBRARIES}")







    IF(NOT WIN32)



        IF( CMAKE_SIZEOF_VOID_P EQUAL 8 )

            INSTALL(    TARGETS ${MODULE_NAME}
                        ARCHIVE DESTINATION lib64
                        LIBRARY DESTINATION lib64)

        ELSE( CMAKE_SIZEOF_VOID_P EQUAL 8 )

            INSTALL(    TARGETS ${MODULE_NAME}
                        ARCHIVE DESTINATION lib
                        LIBRARY DESTINATION lib)

        ENDIF( CMAKE_SIZEOF_VOID_P EQUAL 8 )




    ELSE(NOT WIN32)



        INSTALL(    TARGETS ${MODULE_NAME}
                    RUNTIME DESTINATION bin
                    LIBRARY DESTINATION lib
                    ARCHIVE DESTINATION lib)






    ENDIF(NOT WIN32)




    FOREACH(arg ${TARGET_H})
        FILE(APPEND ${OOD_TEMP_DOXYGEN_INPUT} "${arg}\n")
    ENDFOREACH(arg ${TARGET_H})

    FOREACH(arg ${TARGET_SRC})
        FILE(APPEND ${OOD_TEMP_DOXYGEN_INPUT} "${PROJECT_SOURCE_DIR}/src/${MODULE_NAME}/${arg}\n")
    ENDFOREACH(arg ${TARGET_SRC})


ENDMACRO(OOD_SETUP_LIBRARY)



















MACRO(OOD_SETUP_PLUGIN)

    IF(TARGET_SRC)




    ADD_LIBRARY(    ${MODULE_NAME}
                    ${OOD_USER_DEFINED_DYNAMIC_OR_STATIC}
                    ${TARGET_SRC}
    )




        IF( WIN32 )

            SET(MODULE_LINK_LIBRARIES ${MODULE_LINK_LIBRARIES_WIN})


        ELSE( WIN32 )
            SET(MODULE_LINK_LIBRARIES ${MODULE_LINK_LIBRARIES_GNU})

        ENDIF( WIN32 )




        IF( MODULE_LINK_LIBRARIES )
            STRING(REGEX REPLACE " " ";" MODULE_LINK_LIBRARIES ${MODULE_LINK_LIBRARIES})
        ENDIF( MODULE_LINK_LIBRARIES )



        TARGET_LINK_LIBRARIES(  ${MODULE_NAME}
                                ${MODULE_LINK_LIBRARIES}
        )




        MESSAGE(STATUS "${MODULE_NAME} link libraries: ${MODULE_LINK_LIBRARIES}")





        IF(DYNAMIC_OOD)
            SET_TARGET_PROPERTIES(  ${MODULE_NAME}
                                    PROPERTIES PREFIX "")
        ENDIF(DYNAMIC_OOD)





        IF(NOT WIN32)


            IF( CMAKE_SIZEOF_VOID_P EQUAL 8 )

                INSTALL(TARGETS ${MODULE_NAME}
                        ARCHIVE DESTINATION lib64/osgPlugins-${OOD_OSG_VERSION}
                        LIBRARY DESTINATION lib64/osgPlugins-${OOD_OSG_VERSION})

            ELSE( CMAKE_SIZEOF_VOID_P EQUAL 8 )

                INSTALL(TARGETS ${MODULE_NAME}
                        ARCHIVE DESTINATION lib/osgPlugins-${OOD_OSG_VERSION}
                        LIBRARY DESTINATION lib/osgPlugins-${OOD_OSG_VERSION})

            ENDIF( CMAKE_SIZEOF_VOID_P EQUAL 8 )




        ELSE(NOT WIN32)


            INSTALL(TARGETS ${MODULE_NAME}
                    RUNTIME DESTINATION bin/osgPlugins-${OOD_OSG_VERSION}
                    LIBRARY DESTINATION lib/osgPlugins-${OOD_OSG_VERSION}
                    ARCHIVE DESTINATION lib/osgPlugins-${OOD_OSG_VERSION})


        ENDIF(NOT WIN32)

    ENDIF(TARGET_SRC)


ENDMACRO(OOD_SETUP_PLUGIN)









MACRO(OOD_SETUP_EXAMPLE EXAMPLE_NAME)


    IF(NOT TARGET_TARGETNAME)
            SET(TARGET_TARGETNAME "${TARGET_DEFAULT_PREFIX}${EXAMPLE_NAME}")
    ENDIF(NOT TARGET_TARGETNAME)
    IF(NOT TARGET_LABEL)
            SET(TARGET_LABEL "${TARGET_DEFAULT_LABEL_PREFIX} ${EXAMPLE_NAME}")
    ENDIF(NOT TARGET_LABEL)



    ADD_EXECUTABLE(${TARGET_TARGETNAME} ${TARGET_SRC} ${TARGET_H})



    TARGET_LINK_LIBRARIES(  ${TARGET_TARGETNAME}
                            ${TARGET_COMMON_LIBRARIES}
    )



    SET_TARGET_PROPERTIES(${TARGET_TARGETNAME} PROPERTIES FOLDER "Examples")

#     INSTALL(TARGETS ${TARGET_TARGETNAME} RUNTIME DESTINATION share/ood/bin COMPONENT ood-examples )

ENDMACRO(OOD_SETUP_EXAMPLE)