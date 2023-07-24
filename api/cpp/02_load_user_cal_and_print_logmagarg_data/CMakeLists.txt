cmake_minimum_required(VERSION 3.20)
project(02_load_user_cal_and_sweep)

set(CMAKE_CXX_STANDARD 11)

add_executable(02_load_user_cal_and_sweep main.cpp)

# Set platform-specific include and library directories
# Change these to match the locations of the headers and libraries if you have not installed the PicoVNA 5 software,
# or if you have installed it in a non-standard location.
IF(WIN32)
    # Windows library and include directories
    set(VNA_INCLUDE_DIR "C:/Program Files/Pico Technology Ltd/PicoVNA 5/include")

    # Libraries: need vna.lib
    find_library(VNA_LIB
            NAMES vna
            PATHS "C:/Program Files/Pico Technology Ltd/PicoVNA 5/lib"
    )

    # We must also copy required dlls (vna.dll and ftd2xx.dll) to runtime output directory
    file(GLOB VNA_REQUIRED_DLLS
            "C:/Program Files/Pico Technology Ltd/PicoVNA 5/bin/*.DLL"
            )
    file(COPY ${VNA_REQUIRED_DLLS}
            DESTINATION ${02_load_user_cal_and_sweep_BINARY_DIR})

ELSEIF(APPLE)
    # macOS library and include directories
    set(VNA_INCLUDE_DIR "/Applications/picovna5.app/Contents/MacOS/include")

    # Libraries: need libvna.dylib
    find_library(VNA_LIB
            NAMES vna
            PATHS "/Applications/picovna5.app/Contents/MacOS/lib"
    )
ELSEIF(UNIX)
    # Linux library and include directories
    set(VNA_INCLUDE_DIR "/opt/picovna/include")

    # Libraries: need libvna.so
    find_library(VNA_LIB
            NAMES vna
            PATHS "/opt/picovna/lib"
    )
ENDIF(WIN32)

# Includes: need vna/*.h
target_include_directories(02_load_user_cal_and_sweep PRIVATE ${VNA_INCLUDE_DIR})

# Link
target_link_libraries(02_load_user_cal_and_sweep ${VNA_LIB})
