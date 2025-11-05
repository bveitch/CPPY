from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "array_norm_cpp",  # Module name
        ["binding.cpp"],  # Source files
        include_dirs=["include"],  # cpp headers
        extra_compile_args=['-O3', "-fopenmp"],
        extra_link_args=["-fopenmp"],

    )
]

setup(
    name="array_norm_cpp",
    version="0.1",
    ext_modules=ext_modules,
)