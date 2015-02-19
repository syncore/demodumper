import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, Extension, find_packages

m = Extension('huffman',
              sources = ['huffman/huffman.c','huffman/pyhuffman.c'])

setup (name = 'ql-demo',
       version = '0.4.3',
       ext_modules = [m],
       packages = find_packages(),
       scripts = ['demodumper.py','ez_setup.py'],
       author = "Shawn Nock",
       author_email = "nock@nocko.se",
       description = "Wrapper for Q3A Huffman Code Routines and QuakeLive Demo Utility Classes",
       license = "GPLv3",
       keywords = "quake quakelive demo dm_73 quakecon",
       url = "https://aphr.asia/gitweb/?p=qldemo-python.git;a=summary",
       zip_safe = True
)


