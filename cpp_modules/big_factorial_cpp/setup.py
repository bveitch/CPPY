import os
import platform

# 1. Enforce Homebrew LLVM on Mac
compiler = "clang"
if platform.system() == "Darwin":
    if compiler == "clang":
        os.environ["CC"] = "/opt/homebrew/opt/llvm/bin/clang"
        os.environ["CXX"] = "/opt/homebrew/opt/llvm/bin/clang++"
    else:
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
        "big_factorial_cpp",  # Module name
        ["binding.cpp"],  # Source files
        include_dirs=include_dirs,    # Tells GCC where to find <gmpxx.h>
        library_dirs=library_dirs,    # Tells the linker where to find the library files
        extra_link_args=['-lgmp', '-lgmpxx']

    )
]

setup(
    name="big_factorial_cpp",
    version="0.1",
    ext_modules=ext_modules,
)