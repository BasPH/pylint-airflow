"""Setup of pylint-airflow package"""
from pathlib import Path

from setuptools import setup, find_packages

requirements = ["pylint"]

readme = Path(__file__).resolve().parent / "README.rst"
with open(readme) as f:
    long_description = f.read()

setup(
    name="pylint-airflow",
    url="https://github.com/BasPH/pylint-airflow",
    description="A Pylint plugin to lint Apache Airflow code.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    version="0.1.0-alpha.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    keywords=["pylint", "airflow", "plugin"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
