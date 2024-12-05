from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='LAB2',
        packages=find_packages(where="src"),
        package_dir={"": "src"}
    )
