from setuptools import setup, find_packages

requires = [
    'flask',
    'pandas'
]

setup(
    name='network_statistics',
    version='0.0',
    description='A Firewall Analytics Interface built with Flask',
    author='Cody Buntain',
    author_email='cody@bunta.in',
    keywords='web flask firewall ids',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)