"""
Setup script for MunsellSpace Python package.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Read version from __init__.py
def read_version():
    init_path = os.path.join(os.path.dirname(__file__), "munsellspace", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="munsellspace",
    version=read_version(),
    author="MunsellSpace Contributors",
    author_email="",
    description="High-precision sRGB to Munsell color space conversion with 99.98% reference accuracy",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/chrisgve/MunsellSpace",
    project_urls={
        "Bug Tracker": "https://github.com/chrisgve/MunsellSpace/issues",
        "Documentation": "https://docs.rs/munsellspace",
        "Source Code": "https://github.com/chrisgve/MunsellSpace",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Multimedia :: Graphics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Rust",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Minimal dependencies - the Rust binary handles the core conversion
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "isort",
            "mypy",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ],
    },
    keywords=[
        "color", "munsell", "srgb", "color-science", "conversion", 
        "color-space", "rgb", "graphics", "image-processing"
    ],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "munsellspace=munsellspace.cli:main",
        ],
    },
)