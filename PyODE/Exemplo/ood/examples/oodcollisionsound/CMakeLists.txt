SET(TARGET_SRC oodcollisionsound.cpp  )


IF( WIN32 )
    SET(OOS_INCLUDE "$ENV{PROGRAMFILES}\\oos\\include" CACHE PATH "o.O Sound Headers")
    SET(OPENAL_INCLUDE "$ENV{PROGRAMFILES}\\OpenAL 1.1 SDK\\include" CACHE PATH "OpenAL headers")
    SET(OOS_LIBRARIES "$ENV{PROGRAMFILES}\\oos\\lib" CACHE PATH "o.O Sound Libraries")
    SET(OPENAL_LIBRARIES "$ENV{PROGRAMFILES}\\OpenAL 1.1 SDK\\libs\\Win32" CACHE PATH "OpenAL libraries")

ELSE( WIN32 )
    EXECUTE_PROCESS(COMMAND pkg-config oos --cflags-only-I OUTPUT_VARIABLE tmp_var)
    STRING(REGEX REPLACE "\n" "" tmp_var "${tmp_var}")
    STRING(REGEX REPLACE "-I" "" tmp_var "${tmp_var}")

    SET(OOS_INCLUDE ${tmp_var} CACHE PATH "o.O Sound Headers")

    EXECUTE_PROCESS(COMMAND pkg-config oos --libs-only-L OUTPUT_VARIABLE tmp_var)
    STRING(REGEX REPLACE "\n" "" tmp_var "${tmp_var}")
    STRING(REGEX REPLACE "-L" "" tmp_var "${tmp_var}")

    SET(OOS_LIBRARIES ${tmp_var} CACHE PATH "o.O Sound libraries")



    EXECUTE_PROCESS(COMMAND pkg-config openal --cflags-only-I OUTPUT_VARIABLE tmp_var)
    STRING(REGEX REPLACE "\n" "" tmp_var "${tmp_var}")
    STRING(REGEX REPLACE "-I" "" tmp_var "${tmp_var}")

    SET(OPENAL_INCLUDE ${tmp_var} CACHE PATH "OpenAL Headers")



    EXECUTE_PROCESS(COMMAND pkg-config openal --libs-only-L OUTPUT_VARIABLE tmp_var)
    STRING(REGEX REPLACE "\n" "" tmp_var "${tmp_var}")
    STRING(REGEX REPLACE "-L" "" tmp_var "${tmp_var}")

    SET(OPENAL_LIBRARIES ${tmp_var} CACHE PATH "OpenAL libraries")
ENDIF( WIN32 )

INCLUDE_DIRECTORIES(${OOS_INCLUDE})
INCLUDE_DIRECTORIES(${OPENAL_INCLUDE})
LINK_DIRECTORIES(${OOS_LIBRARIES})
LINK_DIRECTORIES(${OPENAL_LIBRARIES})

SET(TARGET_COMMON_LIBRARIES ${TARGET_COMMON_LIBRARIES} oos)

IF( WIN32 )
    SET(TARGET_COMMON_LIBRARIES ${TARGET_COMMON_LIBRARIES} OpenAL32)
ENDIF( WIN32 )

OOD_SETUP_EXAMPLE( oodcollisionsound )
