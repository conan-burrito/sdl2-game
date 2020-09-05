cmake_minimum_required(VERSION 3.17)

project(sdl2-game LANGUAGES CXX VERSION 0.0.1)

##
## Setup some platform-specific stuff
##
if(IOS)
    set(CMAKE_XCODE_ATTRIBUTE_DEVELOPMENT_TEAM $ENV{XCODE_ATTRIBUTE_DEVELOPMENT_TEAM})
    set(MACOSX_BUNDLE_GUI_IDENTIFIER $ENV{MACOSX_BUNDLE_GUI_IDENTIFIER})
    set(CMAKE_XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY $ENV{XCODE_ATTRIBUTE_CODE_SIGN_IDENTITY})

    enable_language(Swift)
    enable_language(OBJC)

    set(STORYBOARDS
        xcode/storyboards/LaunchScreen.storyboard
    )

    set(ASSETS
        ${CMAKE_CURRENT_LIST_DIR}/xcode/assets/Default.xcassets
    )

    #file(GLOB_RECURSE GLOBBED_ASSETS LIST_DIRECTORIES FALSE "${CMAKE_CURRENT_LIST_DIR}/assets" CONFIGURE_DEPENDS
    #    ${CMAKE_CURRENT_LIST_DIR}/assets/*.png
    #    ${CMAKE_CURRENT_LIST_DIR}/assets/*.wav
    #    ${CMAKE_CURRENT_LIST_DIR}/assets/*.mp3
    #)
    #list(APPEND ASSETS ${GLOBBED_ASSETS})
elseif(ANDROID)
    set(PROFILE_PATH "${CMAKE_CURRENT_LIST_DIR}/profiles/android/${ANDROID_ABI}")
    set(CONAN_ARGS "--profile=${PROFILE_PATH}")
endif()

if(RUN_CONAN)
    execute_process(
        COMMAND conan install --install-folder ${CMAKE_BINARY_DIR} --update ${CMAKE_SOURCE_DIR} ${CONAN_ARGS}
        RESULT_VARIABLE CONAN_RESULT
        OUTPUT_VARIABLE CONAN_STDOUT
        ERROR_VARIABLE CONAN_STDERR
    )
    if(CONAN_RESULT)
        message(FATAL_ERROR "Conan error: ${CONAN_STDERR}")
    else()
        message(STATUS "Conan output: ${CONAN_STDOUT}")
    endif()
endif()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

##
## Create the main build target - our game. Its either a shared library (on Android)
## or an executable with some platform-specific properties
##
if(IOS OR APPLE)
    add_executable(game MACOSX_BUNDLE)
elseif(ANDROID)
    add_library(game SHARED)
else()
    add_executable(game)
endif()

target_sources(game PRIVATE
    src/main.cpp
)

set_target_properties(game
    PROPERTIES
        CXX_STANDARD 17
        CXX_STANDARD_REQUIRED YES
        CXX_EXTENSIONS NO
)

target_include_directories(game PUBLIC ${CMAKE_CURRENT_LIST_DIR}/include)
target_link_libraries(game PUBLIC ${CONAN_LIBS})

if(IOS OR APPLE)
    target_sources(game PRIVATE ${STORYBOARDS} ${ASSETS})

    set_target_properties(game PROPERTIES
        RESOURCE "${STORYBOARDS};${ASSETS}"
        MACOSX_BUNDLE_INFO_PLIST "${CMAKE_CURRENT_LIST_DIR}/xcode/plist.in"
        MACOSX_BUNDLE_SHORT_VERSION_STRING ${CMAKE_PROJECT_VERSION}
        MACOSX_BUNDLE_BUNDLE_VERSION ${CMAKE_PROJECT_VERSION}
    )
endif()
