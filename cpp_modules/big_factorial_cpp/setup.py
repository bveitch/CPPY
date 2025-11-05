from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "big_factorial_cpp",  # Module name
        ["binding.cpp"],  # Source files
        extra_link_args=['-lgmp', '-lgmpxx']

    )
]

setup(
    name="big_factorial_cpp",
    version="0.1",
    ext_modules=ext_modules,
)