from setuptools import setup, find_packages


setup(
    name='LAB2',
    packages=find_packages(where="src"),
    package_dir={"": "src"}
)