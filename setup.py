import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


def readfile(filename):
    with open(filename, encoding="utf-8") as fp:
        filecontents = fp.read()
    return filecontents


setuptools.setup(
    name="autopilot",
    version="0.2.0",
    author="Adam Moss",
    author_email="adam.moss@nottingham.ac.uk",
    description="AutoPilot package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=readfile(
        os.path.join(os.path.dirname(__file__), "requirements.txt")
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True
)
