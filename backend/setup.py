from setuptools import setup, find_namespace_packages

setup(
    name="example_package",
    version="0.1.0",
    author="Tamr Inc.",
    author_email="",
    description="A Custom Tamr Package",
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    python_requires=">=3.6",
)