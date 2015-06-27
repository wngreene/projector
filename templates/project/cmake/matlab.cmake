function (add_mex_file mexName mexSources)
    add_executable(${mexName} ${mexSources})
    target_link_libraries(${mexName} $ENV{MATLAB_ROOT}/bin/glnxa64/libmx.so $ENV{MATLAB_ROOT}/bin/glnxa64/libmex.so $ENV{MATLAB_ROOT}/bin/glnxa64/libmat.so m stdc++)
    include_directories($ENV{MATLAB_ROOT}/extern/include)
    set_target_properties(${mexName} PROPERTIES 
        COMPILE_FLAGS "-fexceptions -fPIC -fno-omit-frame-pointer -DMX_COMPAT_32 -D_GNU_SOURCE -DMATLAB_MEX_FILE -DNDEBUG -pthread -g -std=c++11" 
        LINK_FLAGS " -shared -Wl,--no-undefined "
        OUTPUT_NAME ${mexName}.mexa64 
        RUNTIME_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/matlab)
    install(TARGETS ${mexName} RUNTIME DESTINATION matlab)
    ##Note: mex used -ansi instead of -std=c++11
endfunction()

function(install_mfiles)
    if (ARGN GREATER 1) 
        list(GET ARGV -2 checkword)
    endif()
    if(NOT checkword STREQUAL DESTINATION)
        foreach(mfile ${ARGV})
            get_filename_component(_mfile_name ${mfile} NAME)
            configure_file(${mfile} matlab/${_mfile_name} COPYONLY)
        endforeach(mfile)
        install(FILES ${ARGV} DESTINATION ${PROJECT_BINARY_DIR}/matlab/)
    else()
        list(GET ARGV -1 dest_dir)
        list(REMOVE_AT ARGV -1)
        list(REMOVE_AT ARGV -1)
        #copy the mfiles to the INCLUDE_OUTPUT_PATH (${CMAKE_BINARY_DIR}/include)
        foreach(mfile ${ARGV})
            get_filename_component(_mfile_name ${mfile} NAME)
            configure_file(${mfile} ${INCLUDE_OUTPUT_PATH}/${dest_dir}/${_mfile_name} COPYONLY)
        endforeach(mfile)
        #mark them to be installed
        install(FILES ${ARGV} DESTINATION matlab/${dest_dir})
    endif()
endfunction(install_mfiles)

file(GLOB MFILES "*.m")
install(FILES ${MFILES} DESTINATION matlab/)
