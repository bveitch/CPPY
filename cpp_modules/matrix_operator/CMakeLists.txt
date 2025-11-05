project(matrix_operator_cpp LANGUAGES CXX)
set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
#find_package(OpenMP REQUIRED COMPONENTS CXX)
pybind11_add_module(matrix_operator_cpp binding.cpp)
target_link_libraries(matrix_operator_cpp PUBLIC pybind11::headers)

install(TARGETS matrix_operator_cpp DESTINATION .)
install(TARGETS matrix_operator_cpp DESTINATION .)