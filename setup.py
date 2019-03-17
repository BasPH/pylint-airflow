"""Setup of pylint-airflow package"""

from setuptools import setup, find_packages

requirements = ["pylint"]
dev_requirements = ["apache-airflow~=1.10.2", "black>=18.9b0", "pytest~=4.3"]

setup(
    name="pylint-airflow",
    url="https://github.com/BasPH/pylint-airflow",
    description="A Pylint plugin to lint Apache Airflow code.",
    version="0.1.0-alpha",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    extras_require={"dev": dev_requirements},
    keywords=["pylint", "airflow", "plugin"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
