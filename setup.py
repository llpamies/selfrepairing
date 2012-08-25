from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("selfrepairing", ["selfrepairing.pyx","jerasure.c","galois.c"],
    #include_dirs = ["Jerasure/include"],
    #libraries = ["Jerasure"],
    #library_dirs = ["Jerasure/lib"],
    #extra_compile_args = ["-static"],
)])
