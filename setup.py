# Copyright (c) 2024, Nathan Hansen
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from setuptools import setup

setup(
    name="pydrawnet",
    version="0.1.0",
    description="A utility for drawing neural network and other diagrams",
    url="https://github.com/nhansendev/PyDrawNet",
    author="Nathan Hansen",
    author_email="nato5342@hotmail.com",
    license="BSD 3-clause",
    packages=["pydrawnet"],
    install_requires=["matplotlib"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.14",
    ],
)
