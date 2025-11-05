#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "array_norm.hpp"
namespace py = pybind11;

PYBIND11_MODULE(array_norm_cpp, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: array_norm_cpp

        .. autosummary::
           :toctree: _generate

           norm of numpy array

    )pbdoc";

    m.def("l2_norm", &l2norm<double, double>, R"pbdoc(
        l2 norm of an array
    )pbdoc");
    m.def("l2_norm_omp", &l2norm_omp<double, double>, R"pbdoc(
        l2 norm of an array using openmp reduction
    )pbdoc");
    m.def("func_norm", &py_functional_norm<double, double>, R"pbdoc(
        functional norm of an array using a python function
    )pbdoc");

}