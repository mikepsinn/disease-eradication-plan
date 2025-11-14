#!/usr/bin/env python3
"""
Setup configuration for dih-economic-models package.
Makes economic_parameters and helper modules importable from anywhere.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read dependencies from requirements if exists
requirements = []
req_file = Path(__file__).parent / "requirements.txt"
if req_file.exists():
    requirements = req_file.read_text().strip().split('\n')

setup(
    name="dih-economic-models",
    version="1.0.0",
    description="Economic analysis and ROI calculations for the 1% Treaty and dFDA",
    author="Mike P. Sinn",
    author_email="hello@dih.earth",
    url="https://models.dih.earth",
    packages=find_packages(),
    py_modules=[
        'economic_parameters',
    ],
    package_data={
        '': ['*.qmd', '*.py', '*.yml'],
    },
    install_requires=[
        'matplotlib>=3.5.0',
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'graphviz>=0.20.0',
        'ipython>=8.0.0',
        'pillow>=9.0.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
