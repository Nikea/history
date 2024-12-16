from setuptools import setup

setup(name='historydict',
      version='1.2.7',
      author='Brookhaven National Laboratory',
      py_modules=['historydict'],
      description='A persistent dictionary with history backed by sqlite',
      url='http://github.com/Nikea/historydict',
      platforms='Cross platform (Linux, Mac OSX, Windows)',
      license_files=('LICENSE.',),
      classifiers = [
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3.11",
          "Programming Language :: Python :: 3.12",
          "Programming Language :: Python :: 3.13",
      ],
      install_requires=['setuptools'],
      )
