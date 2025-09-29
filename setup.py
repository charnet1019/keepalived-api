import os
import sys
from setuptools import setup, find_packages

PACKAGE_NAME = "keepalived-api"

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def fread(file) -> str:
    # First try to read from current working directory (for sdist builds)
    try:
        with open(file, "r") as f:
            return f.read()
    except FileNotFoundError:
        # If that fails, try with ROOT_DIR (for development)
        file_path = os.path.join(ROOT_DIR, file)
        with open(file_path, "r") as f:
            return f.read()


setup(
    name="keepalived-api",
    version=fread("VERSION").strip(),
    long_description=fread("README.md").strip(),
    long_description_content_type="text/markdown",
    author="charnet1019",
    url="https://github.com/charnet1019/keepalived-api",
    license=fread("LICENSE").strip(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.10",
)