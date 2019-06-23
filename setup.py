
from setuptools import setup, find_packages

config = {
    'description': 'Weather data aggregator and analyzer',
    'author': 'ross palmer',
    'url': 'https://github.com/rosspalmer/IdealSpot',
    'license': 'MIT',
    'version': '0.1.0',
    'install_requires': ['pandas'],
    'packages': find_packages(),
    'scripts': [],
    'name': 'ideal_spot'
}

setup(**config)
