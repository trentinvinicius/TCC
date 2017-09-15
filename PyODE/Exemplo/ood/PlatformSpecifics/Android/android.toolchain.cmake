# Cross-compiling requires CMake 2.6 or newer. Example:
# cmake .. -DCMAKE_TOOLCHAIN_FILE=../XCompile-Android.txt -DHOST=arm-linux-androideabi
# Where 'arm-linux-androideabi' is the host prefix for the cross-compiler. If
# you already have a toolchain file setup, you may use that instead of this
# file. Make sure to set CMAKE_FIND_ROOT_PATH to where the NDK toolchain was
# installed (e.g. "$ENV{HOME}/toolchains/arm-linux-androideabi-r10c-21").

# this one is important
if( CMAKE_VERSION VERSION_GREATER "3.0.99" )
 set( CMAKE_SYSTEM_NAME Android )
else()
 set( CMAKE_SYSTEM_NAME Linux )
endif()

# the name of the target operating system
if( CMAKE_VERSION VERSION_GREATER "3.0.99" )
 set( CMAKE_SYSTEM_NAME Android )
else()
 set( CMAKE_SYSTEM_NAME Linux )
endif()

# which compilers to use for C and C++
set( CMAKE_C_COMPILER    "${HOST}-gcc"      CACHE PATH "C compiler")
set( CMAKE_CXX_COMPILER  "${HOST}-g++"      CACHE PATH "C++ compiler")
set( CMAKE_RC_COMPILER   "${HOST}-windres"  CACHE PATH "windres")
set( CMAKE_ASM_COMPILER  "${HOST}-gcc"      CACHE PATH "assembler" )
set( CMAKE_STRIP         "${HOST}-strip"    CACHE PATH "strip" )
set( CMAKE_AR            "${HOST}-ar"       CACHE PATH "archive" )
set( CMAKE_LINKER        "${HOST}-ld"       CACHE PATH "linker" )
set( CMAKE_NM            "${HOST}-nm"       CACHE PATH "nm" )
set( CMAKE_OBJCOPY       "${HOST}-objcopy"  CACHE PATH "objcopy" )
set( CMAKE_OBJDUMP       "${HOST}-objdump"  CACHE PATH "objdump" )
set( CMAKE_RANLIB        "${HOST}-ranlib"   CACHE PATH "ranlib" )

# adjust the default behaviour of the FIND_XXX() commands:
# search headers and libraries in the target environment, search
# programs in the host environment
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
