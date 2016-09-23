import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='floss-agricultural-simulation',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Farm Level Open Source Simulation',
    long_description=README,
    url='https://github.com/BenLatham/FLOSS-Agricultural-Simulation',
    author='Ben Latham',
    author_email='ben.latham@malachitedesign.co.uk',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.1',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
