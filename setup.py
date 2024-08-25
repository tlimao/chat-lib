from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    package_paths = {}

    for package in find_packages():
        package_paths[package] = "/".join(package.split("."))

setup(
    name='freedom-lib',
    version='1.0.0',
    url='https://github.com/tlimao/freedom-lib',
    author='@w!l',
    author_email='tloime@gmail.com',
    description='Freedom lib',
    package_data={"freedom-lib": ["py.typed"]},
    packages=find_packages(),
    package_dir=package_paths,
    install_requires=requirements,
    python_requires='>=3.6',
    tests_require=[
        'pytest>=8.3.2',
        'coverage>=5.5',
    ],
)