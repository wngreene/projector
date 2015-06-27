cmake_minimum_required(VERSION 2.8)

#-------------------------------------------------------------------------------
# Project initialization.
#-------------------------------------------------------------------------------

project(project)
set(${PROJECT_NAME}_VERSION 0.0.1)

# Options.
option(BUILD_DOCUMENTATION "Use Doxygen to create the HTML based API documentation" ON)
option(BUILD_TESTS "Use GTest to build and test libraries" ON)

# CMake includes.
include(cmake/setup.cmake)
include(cmake/install.cmake)

# Locate external dependencies
# find_package(Eigen3 3.2 EXACT REQUIRED)
# find_package(OpenCV 2.4.9 EXACT REQUIRED core highgui imgproc) 

# Project includes
# include_directories(src)
# include_directories(SYSTEM ${EIGEN3_INCLUDE_DIR} ${OpenCV_INCLUDE_DIRS})

#-------------------------------------------------------------------------------
# Build, install, and configure a library.
#-------------------------------------------------------------------------------

# Build the library
# set(MY_LIBRARY_NAME project)
# file(GLOB_RECURSE MY_LIBRARY_SRCS "src/project/*.cc")
# add_library(${MY_LIBRARY_NAME} SHARED ${MY_LIBRARY_SRCS})
# target_link_libraries(${MY_LIBRARY_NAME})
# set_target_properties(${MY_LIBRARY_NAME} PROPERTIES 
#     COMPILE_FLAGS "-std=c++11 -Wall")

# Install the library and header files
# install(TARGETS ${MY_LIBRARY_NAME} 
#   RUNTIME DESTINATION bin
#   LIBRARY DESTINATION lib
#   ARCHIVE DESTINATION lib)
# install(DIRECTORY src/${PROJECT_NAME} DESTINATION include
#   FILES_MATCHING PATTERN "*.h")

# Configure the library

# Configuration method 1: pkg_config
# install_pkg_config_file(${PROJECT_NAME}
#   DESCRIPTION "An example project."
#   LIBS -l${MY_LIBRARY_NAME}
#   VERSION ${${PROJECT_NAME}_VERSION}
#   REQUIRES
#   CFLAGS "-std=c++11")

# Configuration method 2: pure cmake, no import/export
# NOTE: You need to edit the config file (${PROJECT_NAME}Config.cmake.in) manually!
# configure_file(cmake/templates/${PROJECT_NAME}Config.cmake.in
#   "${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}Config.cmake" @ONLY)
# configure_file(cmake/templates/${PROJECT_NAME}ConfigVersion.cmake.in
#   "${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}ConfigVersion.cmake" @ONLY)
# install(FILES 
#   ${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}Config.cmake 
#   ${PROJECT_BINARY_DIR}/lib/cmake/${PROJECT_NAME}ConfigVersion.cmake 
#   DESTINATION ${CMAKE_MODULE_PATH})

#-------------------------------------------------------------------------------
# Build and install an executable.
#-------------------------------------------------------------------------------

# set(MY_EXECUTABLE_NAME example)
# set(MY_EXECUTABLE_SRC src/example.cc)
# add_executable(${MY_EXECUTABLE_NAME} ${MY_EXECUTABLE_SRC})
# target_link_libraries(${MY_EXECUTABLE_NAME} ${MY_LIBRARY_NAME})
# set_target_properties(${MY_EXECUTABLE_NAME} PROPERTIES 
#     COMPILE_FLAGS "-std=c++11 -Wall")

# Install the executable.
# install(TARGETS ${MY_EXECUTABLE_NAME}
#   RUNTIME DESTINATION bin
#   LIBRARY DESTINATION lib 
#   ARCHIVE DESTINATION lib)

#-------------------------------------------------------------------------------
# Build the unit tests.
#-------------------------------------------------------------------------------

# If the BUILD_TESTS option is set, a Google test binary will be compiled.
if (BUILD_TESTS)
    include(cmake/tests.cmake)

    # file(GLOB TEST_SOURCES "test/*.cc")
    # add_gtest(test_${PROJECT_NAME} ${TEST_SOURCES})
    # target_link_libraries(test_${PROJECT_NAME} ${MY_LIBRARY_NAME})
    # set_target_properties(test_${PROJECT_NAME} PROPERTIES 
    #   COMPILE_FLAGS "-std=c++11 -Wno-deprecated-register")

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
