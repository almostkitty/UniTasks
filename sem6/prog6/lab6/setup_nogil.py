from setuptools import setup
from Cython.Build import cythonize

setup(
    name="cy_fermat_nogil",
    ext_modules=cythonize("cy_fermat_nogil.pyx", annotate=True, language_level=3),
)
