from pathlib import Path
import pathlib
import setuptools
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="nlpytools",
    version="0.1.0",
    description="A set of python tools for Natural Language Processing",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Sirsirious/NLPTools",
    author="Tiago Duque",
    author_email="tfduque@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["sklearn-crfsuite", "numpy", "tqdm", "symspellpy"],
    entry_points={
    },
)
