# Standard library imports
from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="galois-shannon-fano",
    version="1.0.0",
    description="Shannon-Fano coding with Galois Fields for error correction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Flavio A Campos",
    author_email="your.email@example.com",  # Update this
    url="https://github.com/FlavioACampos/galois-shannon-fano",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.0.0",
        "matplotlib>=3.3.0",
        "networkx>=2.5",
        "jupyter>=1.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    keywords="shannon-fano, galois-fields, error-correction, coding-theory",
)