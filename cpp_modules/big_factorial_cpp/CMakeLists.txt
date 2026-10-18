cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)
set(PYBIND11_FINDPYTHON ON)
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

pybind11_add_module(${SKBUILD_PROJECT_NAME} binding.cpp)
target_include_directories(${SKBUILD_PROJECT_NAME} PRIVATE "${GMP_INCLUDE_DIR}")
target_link_libraries(${SKBUILD_PROJECT_NAME} PRIVATE "${GMP_LIBRARY}")
install(TARGETS ${SKBUILD_PROJECT_NAME} DESTINATION .)