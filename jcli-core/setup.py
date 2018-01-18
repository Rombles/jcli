from setuptools import setup, find_packages

setup(
    name="jcli_core",
    version="1.0",
    author="BluVector",
    author_email="info@bluvector.io",
    url="https://bluvector.io",
    description="Tool for quickly building BV platform based off of git state",
    long_description="Builds Images, and infrastructure metadata for building \
    the BV platform based off of git state",
    license="Proprietary",
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': ['jcli=jcli_core.cli:main']
    }
)
