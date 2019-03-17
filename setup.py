"""Setup of pylint-airflow package"""

from setuptools import setup, find_packages

requirements = ["pylint"]

setup(
    name="pylint-airflow",
    url="https://github.com/BasPH/pylint-airflow",
    description="A Pylint plugin to lint Apache Airflow code.",
    version="0.1.0-alpha",
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
