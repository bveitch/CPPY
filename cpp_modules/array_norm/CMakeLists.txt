cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP REQUIRED COMPONENTS CXX)
set(CMAKE_CXX_FLAGS "-O3 -fopenmp")
pybind11_add_module(array_norm_cpp binding.cpp)
target_include_directories(array_norm_cpp PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
target_link_libraries(array_norm_cpp PRIVATE OpenMP::OpenMP_CXX)
target_link_libraries(array_norm_cpp PUBLIC pybind11::headers)

install(TARGETS array_norm_cpp DESTINATION .)
install(TARGETS array_norm_cpp DESTINATION .)