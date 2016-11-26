#!/usr/bin/env python3

from setuptools import setup


setup(
    name='pyfrcsim',
    version='0.1.0',
    description='FRCSim implementation for robotpy',
    long_description='FRCSim implementation for robotpy',
    author='Dustin Spicuzza, Ellery Newcomer',
    author_email='ellery-newcomer@utulsa.edu',
    url='https://github.com/ariovistus/pyfrcsim',
    keywords='frc first robotics hal gazebo',
    packages=[
        'pyfrcsim',
        'pyfrcsim.gazebo',
        'pyfrcsim.gazebo.msgs',
        'pyfrcsim.gazebo.gz_msgs',
        'pyfrcsim.types',
    ],
    entry_points={
        'robotpy': [
            'frcsim = pyfrcsim.main:FrcSimMain',
        ]
    },
    install_requires=[
        'robotpy-hal-sim', # 2017 something or another
        'protobuf==3.1.0.post1',
        'six==1.10.0',
    ],
    license='BSD License',
    classifiers=[
        "Intended Audience :: Education",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Scientific/Engineering"
    ],
)
