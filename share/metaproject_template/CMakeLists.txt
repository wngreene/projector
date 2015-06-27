cmake_minimum_required(VERSION 2.8)

if (NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING
    "Choose the type of build: Debug|Release|RelWithDebInfo|MinSizeRel." FORCE)
endif()

if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/install CACHE PATH "${PROJECT_NAME} install prefix" FORCE)
endif()
message(STATUS "Installing to ${CMAKE_INSTALL_PREFIX}")

option(BUILD_DOCUMENTATION "Use Doxygen to create the HTML based API documentation" ON)
option(BUILD_TESTS "Use GTest to build and test libraries" ON)
option(BUILD_EXAMPLES "Build examples demonstrating how to use the API." ON)

include(cmake/submodule.cmake)

# Submodules.
