cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)
set(PYBIND11_FINDPYTHON ON)
set(CMAKE_CXX_FLAGS "-O3 -fopenmp")
find_package(pybind11 CONFIG REQUIRED)
find_path(GMP_INCLUDE_DIR
    NAMES gmp.h
    PATHS "${GMP_ROOT}/include"
    REQUIRED
)

find_library(GMP_LIBRARY
    NAMES gmp
    PATHS "${GMP_ROOT}/lib"
    REQUIRED
)

pybind11_add_module(big_factorial_cpp binding.cpp)
target_include_directories(big_factorial_cpp PRIVATE "${GMP_INCLUDE_DIR}")
target_link_libraries(big_factorial_cpp PRIVATE "${GMP_LIBRARY}")
target_link_libraries(big_factorial_cpp PUBLIC pybind11::headers)
install(TARGETS big_factorial_cpp DESTINATION .)