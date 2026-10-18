cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP REQUIRED COMPONENTS CXX)
set(CMAKE_CXX_FLAGS "-O3 -fopenmp")
pybind11_add_module(${SKBUILD_PROJECT_NAME} binding.cpp)
target_include_directories(${SKBUILD_PROJECT_NAME} PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
target_link_libraries(${SKBUILD_PROJECT_NAME} PRIVATE OpenMP::OpenMP_CXX)
target_link_libraries(${SKBUILD_PROJECT_NAME} PUBLIC pybind11::headers)

install(TARGETS ${SKBUILD_PROJECT_NAME} DESTINATION .)
install(TARGETS ${SKBUILD_PROJECT_NAME} DESTINATION .)