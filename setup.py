from setuptools import setup, find_packages
import io

with io.open("README.md", encoding='utf-8') as f:
    long_description = f.read()

install_requests = {
    "selenium",
    "PyYAML",
    "xrld",
}

setup(
    name='SelenPyTest',
    version='1.0',
    description='auto test by selenium',
    long_description=long_description,
    author='jason',
    install_requests=install_requests,
    python_requires="3.4, 3.5, 3.6, 3.7",
    packages=find_packages(),
    include_package_data=True,
)
