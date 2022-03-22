from setuptools import setup, find_packages

setup(
    name="pyTWTL",
    version="1.0",
    package_dir={"": "."},
    packages=find_packages(where='.'),
    python_requires=">=3.8",
    install_requires=[
        'pyYAML >= 6.0',
        'networkx >= 2.7.1'
    ]
)