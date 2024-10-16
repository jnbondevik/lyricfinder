from setuptools import setup, find_packages

setup(
    name='lyricfinder',
    version='2.0',
    packages=find_packages(),
    package_data={'source': ['apikey']},
    install_requires=[
        'requests'
      ],
    entry_points={
      'console_scripts': ['lyricfinder=source.main:main']
    }
)