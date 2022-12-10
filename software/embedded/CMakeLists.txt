# The following lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.5)

include($ENV{IDF_PATH}/tools/cmake/project.cmake)

#set(EXTRA_COMPONENT_DIRS components/model/)
#set(EXTRA_COMPONENT_DIRS components/model/edge-impulse-sdk/porting/espressif/)
#add_subdirectory(${CMAKE_SOURCE_DIR}/components/model)
#include_directories(${CMAKE_SOURCE_DIR}/components/model)
#set(EXTRA_COMPONENT_DIRS components/model/edge-impulse-sdk/porting/espressif/ESP-NN/)


#set(EXTRA_COMPONENT_DIRS components/arduino/libraries/ML_Model/edge-impulse-sdk/)
project(led_blinky)
#include_directories(${CMAKE_SOURCE_DIR}/components/model/edge_impulse_sdk)
#target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_SOURCE_DIR}/components/model)     
