import os
import platform

# 1. Enforce Homebrew GCC on Mac
if platform.system() == "Darwin":
    os.environ["CC"] = "/opt/homebrew/bin/gcc-15"
    os.environ["CXX"] = "/opt/homebrew/bin/g++-15"

# 2. Configure paths for Homebrew dependencies like GMP
include_dirs = []
library_dirs = []

if platform.system() == "Darwin":
    # Point GCC to Homebrew's location on Apple Silicon Mac
    include_dirs.append("/opt/homebrew/include")
    library_dirs.append("/opt/homebrew/lib")
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