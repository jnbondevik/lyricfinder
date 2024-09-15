from setuptools import setup, find_packages

setup(
    name="lyricfinder",
    version="1.0",
    packages=find_packages(),
    install_requires=[
      'argparse',
      'bs4',
      'requests'
      ],
    entry_points={
      'console_scripts': ['lyricfinder=source.main:main']
    }
)
