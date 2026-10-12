# CPPY : Calling C++ in Python. Experiments with Pybind11
 
## What
[Pybind11](https://pybind11.readthedocs.io/en/stable/index.html) is a lightweight header-only library that exposes C++ types in Python and vice versa. Amongst the main advantages to using Pybind11 over its competitors are ease of use and that it supports modern C++ (> C++11) and the STL. In this project I have explored the use of Pybind11 as a means to bind and call small C++ libraries in Python.
 
## Why
Python is becoming increasingly popular as a generic scientific programming language. It is ideal for orchestration and passing high level tasks. C++ on the other hand offers more direct memory management and therefore a potential increase in efficiency. Being able to combine the two is a useful functionality. This is particularly true in inverse problems, parsing operator calls and performing simple algebraic calculations on their results is the task of the solver. These calculations are implemented in many python libraries, eg [scipy](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.optimize.minimize.html). The operators themselves can be heavy tasks requiring multiple nodes and threads. These calculations possibly should be performed in C++.
 
## Why not
There is a risk of rebuilding the wheel worse than it is already built elsewhere. Many Python libraries already have efficient code built in C/C++ underneath. Check first that what you need doesn't already exist!
 
## Examples
I provide three examples,
1. Calculating the L2 norm of an array. A very simple example showing how to access numpy arrays in C++ through the buffer protocol.
2. Calculating the factorial of a number $n$. Also ridiculously simple but it shows how to bind C++ libraries, in this case GMP, into Python to provide multi-precision.
> [NOTE!] A more efficient means of evaluating n! is Legendre's method. It is more efficient because we only need to sieve for the primes $<=n$. _Hint: how many zeros appear in 200!_ ?
 
3. A matrix operator suite with openmp support. This is sort of the main point.
 
## Installation
```
conda env create -f environment.yaml
```
```
conda activate cppy
```
To install individual cpp modules,
```
pip install -e ./cpp_modules/[choose_module]
```
To install with ```setuptools``` [deprecated]
```bash
cd cpp_modules/matrix_operator
python setup.py build
python setup.py install
```
Should install folders build, dist, including .lib.so and .egg respectively
[!NOTE] Due to problems with ```clang++``` the modules currently fail to build on a Mac. ***A work in progress!*** In any case you would need to first install gmp and openmp, say by,
```bash
brew install gmp
brew install openmp
```
 
## Running the tests
Run the following script for the `matrix` package:
```bash
cd py/matrix
python test_pylops_binding.py
```
 
## ToDo
 - Consolidate tests with pytest
 - Add a comparison of an L2 solver calling a wrapped cpp matrix operator. Compare this to a direct solve in Python using the underlying numpy array/matrix. These *should* agree!
 - Fix ```clang``` issues!
 - Deprecate setup.py. Note this means moving to ```scikit-build-core```


