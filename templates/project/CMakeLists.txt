cmake_minimum_required(VERSION 2.8)

#-------------------------------------------------------------------------------
# Introduction.
#-------------------------------------------------------------------------------

# This is the top-level CMakeLists.txt file for module_example.
# It will:
#   1. Build, install, and configure a library (rrt).
#   2. Build and install an executble (rrt_gui).
#   3. Build unit tests (test_rrt).
# 
# The build process follows the standard CMake convention:
#    cd module_example
#    mkdir build
#    cd build
#    cmake ..
#    make 
#    make install

#-------------------------------------------------------------------------------
# Project initialization.
#-------------------------------------------------------------------------------

# Here we tell cmake that we want to make a project called "rrt", which will 
# automatically create a variable called PROJECT_NAME (set to "rrt"). We then 
# tell CMake the version number of the project.
project(rrt)
set(${PROJECT_NAME}_VERSION 0.1.1)

# Options
# Specify any custom command-line flags that you want to pass to CMake here.
# For example, if the user calls cmake with "cmake -DBUILD_TESTS", then the 
# BUILD_TESTS variable will be set to TRUE/ON and appropriate action will take
# place.
option(BUILD_DOCUMENTATION "Use Doxygen to create the HTML based API documentation" ON)
option(BUILD_TESTS "Use GTest to build and test libraries" ON)

# CMake includes
# module_example is packaged with some helper CMake functions. We include
# them here so that we can use them.
include(cmake/setup.cmake)
include(cmake/install.cmake)

# Locate external dependencies
# module_example requires some external projects. We locate them here using
# find_package(). If the external project was configured using pkg-config
# instead of CMake, use the FindPkgConfig module instead.
find_package(Eigen3 3.2 EXACT REQUIRED)
find_package(OpenCV 2.4.9 EXACT REQUIRED core highgui imgproc) 

# Project includes
# We set the include directories for the project that are needed to compile
# the library and the executable.
include_directories(SYSTEM ${EIGEN3_INCLUDE_DIR} ${OpenCV_INCLUDE_DIRS})
include_directories(src)

#-------------------------------------------------------------------------------
# Build, install, and configure a library.
#-------------------------------------------------------------------------------

# Build the library
# Here the specify the commands needed to compile the library.
# We put the library name into a variable for clarity. We then
# declare the source files needed for the library, and then call
# the add_library() command with the SHARED option to create a 
# shared object (dynamically-linked library). We then link the library
# we just created with the external libraries specified by our external
# projects using target_link_libraries(). Finally, we set some target
# properties.
set(MY_LIBRARY_NAME rrt)
set(MY_LIBRARY_SRCS src/rrt/rrt.cc 
  src/rrt/map.cc src/rrt/tree.cc)
add_library(${MY_LIBRARY_NAME} SHARED ${MY_LIBRARY_SRCS})
target_link_libraries(${MY_LIBRARY_NAME} ${OpenCV_LIBS})
set_target_properties(${MY_LIBRARY_NAME} PROPERTIES 
    COMPILE_FLAGS "-std=c++11 -Wall")

# Install the library and header files
# We've built the library, but we heven't put it anywhere useful.
# The install command copies the library to the directory set by
# CMAKE_INSTALL_PREFIX (by default it is set to the source folder).
# We install the header files to CMAKE_INSTALL_PREFIX/include.
install(TARGETS ${MY_LIBRARY_NAME} 
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib)
install(DIRECTORY src/${PROJECT_NAME} DESTINATION include
  FILES_MATCHING PATTERN "*.h")

# Configure the library
# We've built the library and installed it, but we haven't told anyone else
# where to find it. The configuration process allows other users to find out
# where the library was installed and which headers/libraries to include 
# in order to use it.

# Configuration method 1: pkg_config
install_pkg_config_file(${PROJECT_NAME}
  DESCRIPTION "An example module implementing an RRT"
  LIBS -l${MY_LIBRARY_NAME}
  VERSION ${${PROJECT_NAME}_VERSION}
  REQUIRES eigen3
  CFLAGS "-std=c++11")

# Configuration method 2: pure cmake, no import/export
# NOTE: You need to edit the config file (${PROJECT_NAME}Config.cmake.in) manually!
configure_file(cmake/templates/${PROJECT_NAME}Config.cmake.in
  "${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}Config.cmake" @ONLY)
configure_file(cmake/templates/${PROJECT_NAME}ConfigVersion.cmake.in
  "${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}ConfigVersion.cmake" @ONLY)
install(FILES 
  ${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}Config.cmake 
  ${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}ConfigVersion.cmake 
  DESTINATION ${CMAKE_MODULE_PATH})

#-------------------------------------------------------------------------------
# Build and install an executable.
#-------------------------------------------------------------------------------

# Now we're ready to build an exexutable that uses the library we just
# created. First we specify the executable name and source files in variables
# for clarity. We then create the executable with the add_executable() command.
# Next, we link the executable to both the generated library as well as the
# external libraries. Finally, we set some target properties.
set(MY_EXECUTABLE_NAME rrt_gui)
set(MY_EXECUTABLE_SRC src/rrt_gui.cc)
add_executable(${MY_EXECUTABLE_NAME} ${MY_EXECUTABLE_SRC})
target_link_libraries(${MY_EXECUTABLE_NAME} ${OpenCV_LIBS} ${MY_LIBRARY_NAME})
set_target_properties(${MY_EXECUTABLE_NAME} PROPERTIES 
    COMPILE_FLAGS "-std=c++11 -Wall")

# Install the executable.
# We've built an executable, but we haven't placed it anywhere useful.
# The install() command will place the binary file into CMAKE_INSTALL_PREFIX/bin.
install(TARGETS ${MY_EXECUTABLE_NAME}
  RUNTIME DESTINATION bin
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib)

#-------------------------------------------------------------------------------
# Build the unit tests.
#-------------------------------------------------------------------------------

# If the BUILD_TESTS option is set, a Google test binary will be compiled.
if (BUILD_TESTS)
    include(cmake/tests.cmake)

    file(GLOB TEST_SOURCES "test/*.cc")
    add_gtest(test_${PROJECT_NAME} ${TEST_SOURCES})
    target_link_libraries(test_${PROJECT_NAME} ${MY_LIBRARY_NAME})
    set_target_properties(test_${PROJECT_NAME} PROPERTIES 
      COMPILE_FLAGS "-std=c++11 -Wno-deprecated-register")

    # add_each_test()
    # add_all_tests()
endif()

if (BUILD_DOCUMENTATION)
    find_package(Doxygen)

    if (NOT DOXYGEN_FOUND)
        message(FATAL_ERROR
        "Doxygen is needed to build the documentation.")
    endif()

    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/doc/Doxyfile.in
       ${CMAKE_CURRENT_BINARY_DIR}/doc/Doxyfile @ONLY)
    add_custom_target(doc ALL
       ${DOXYGEN_EXECUTABLE} ${CMAKE_CURRENT_BINARY_DIR}/doc/Doxyfile
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/doc
    COMMENT "Generatin API documentation with Doxygen" VERBATIM
    )
    install(DIRECTORY ${CMAKE_BINARY_DIR}/doc/html DESTINATION doc)
    install(DIRECTORY ${CMAKE_BINARY_DIR}/doc/latex DESTINATION doc)
endif()
