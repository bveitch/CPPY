#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <numeric>
#include <gmpxx.h>

namespace py = pybind11;
using namespace std;

template<typename T>
T factorial_recursive(const T& n){
    if ( n==T(1) ){
        return T(1);
    }
    else if( n < T(1)){
        return 0;
    }
    else{
        return n*factorial_recursive(T(n-1));
    }
}

py::str mpz_factorial(const py::str& py_string){
   mpz_class bignum =  mpz_class(py_string.cast<std::string>());
   mpz_class bigresult = factorial_recursive(bignum);
   return bigresult.get_str();
}

PYBIND11_MODULE(big_factorial_cpp, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: big_factorial_cpp

        .. autosummary::
           :toctree: _generate

           factorial

    )pbdoc";

    m.def("factorial", &mpz_factorial, R"pbdoc(
        convert python str to mpz_class
        take factorial 
        convert back to python str
    )pbdoc");

}