# Force GCC/G++ before importing setuptools
import os
import sys
os.environ["CC"] = "/opt/homebrew/bin/gcc-15"
os.environ["CXX"] = "/opt/homebrew/bin/g++-15"
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "matrix_operator_cpp",  # Module name
        ["binding.cpp"],  # Source files
        include_dirs=["include"],  # cpp headers
        extra_compile_args=['-O3', "-fopenmp"],
        extra_link_args=["-fopenmp"],
    )
]

setup(
    name="matrix_operator_cpp",
    version="0.1",
    ext_modules=ext_modules,
)