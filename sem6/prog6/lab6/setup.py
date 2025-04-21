from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cy_fermat",
    ext_modules=cythonize("cy_fermat.pyx", annotate=True),
)