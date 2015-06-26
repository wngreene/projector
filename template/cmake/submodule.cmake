# This file defines a convenience function, add_submodule(), for including 
# cmake based projects, and also adds a single target---reconfigure---which 
# will force reconfiguration of any module added with add_submodule()
include(ExternalProject)
add_custom_target(reconfigure)

# Function to simplify building collections of modules
# Usage: add_submodule(target [DIRECTORY path/to/target/] [DEPENDS ...])
#   target: name of submodule
#   Optional arguments:
#     DIRECTORY: location of module relative to project root. 
#                Defaults to ${target}
#     DEPENDS: list of other modules created by add_submodule on which to 
#              depend
# 
# Once called, defines the following targets:
#     ${target}: build the module by switching to its binary_directory and 
#        calling make
#     ${target}_reconfigure: Delete the contents of the module build directory 
#        and force reconfiguration on the next invocation of make ${target}
# 
# The submodule is passed the following CMake arguments:
#    CMAKE_INSTALL_PREFIX (PATH)
#    CMAKE_BUILD_TYPE (STRING) 
#    BUILD_DOCUMENTATION (BOOL) 
#    BUILD_TESTS (BOOL)
#    BUILD_EXAMPLES (BOOL)
#
# example:
#   add_submodule(example 
#         DIRECTORY submodules/example 
#         DEPENDS lib1 module2)
function (add_submodule MODULE )
  # Parse arguments: we accept a directory if the module is not located at the 
  # top level,  and a list of projects on which the module depends.
  set(modewords DIRECTORY DEPENDS)
  set(curmode "")
  set(SOURCE_DIR ${CMAKE_SOURCE_DIR}/${MODULE}) 
  list(REMOVE_AT ARGV 0)
  foreach(word ${ARGV})
    list(FIND modewords ${word} mode_index)
    if(${mode_index} GREATER -1)
      set(curmode ${word})
    elseif(curmode STREQUAL DIRECTORY)
      set(SOURCE_DIR ${CMAKE_SOURCE_DIR}/${word}) 
      set(curmode "")
    elseif(curmode STREQUAL DEPENDS)
      list(APPEND _depends ${word})
    else(${mode_index} GREATER -1)
      message("WARNING incorrect use of add_submodule (${word})")
      break()
    endif(${mode_index} GREATER -1)
  endforeach(word)

  # Add the module as an external project.  CMake uses bizarre defaults that 
  # involve several copies of the source---so override those with something sane.
  ExternalProject_Add(${MODULE}
    PREFIX ${SOURCE_DIR}
    TMP_DIR ${CMAKE_BINARY_DIR}/CMakeFiles/tmp
    STAMP_DIR ${CMAKE_BINARY_DIR}/CMakeFiles/stamp
    DOWNLOAD_DIR ${SOURCE_DIR}
    SOURCE_DIR ${SOURCE_DIR}
    BINARY_DIR ${SOURCE_DIR}/build
    INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
    CMAKE_ARGS -DBUILD_DOCUMENTATION:BOOL=${BUILD_DOCUMENTATION}
    -DBUILD_TESTS:BOOL=${BUILD_TESTS}
    -DBUILD_EXAMPLES:BOOL=${BUILD_EXAMPLES}
    -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
    -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    DEPENDS ${_depends}
    )

  # Poke the build to force it to call make every time.
  ExternalProject_Add_Step(${MODULE} poke
    DEPENDERS build
    ALWAYS 1
    )

  # Add a target to force reconfiguration
  add_custom_target(${MODULE}_reconfigure rm -rf ${SOURCE_DIR}/build/*
    COMMAND rm -f ${CMAKE_BINARY_DIR}/CMakeFiles/stamp/${MODULE}-configure
    )
  add_dependencies(reconfigure ${MODULE}_reconfigure)
endfunction()
