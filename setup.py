"""Setup of pylint-airflow package"""

from setuptools import setup, find_packages

ci = ["pytest~=4.3", "black>=18.9b0", "apache-airflow~=1.10.2"]

setup(
    name="pylint-airflow",
    url="https://github.com/BasPH/pylint-airflow",
    description="A Pylint plugin to lint Apache Airflow code.",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pylint"],
    keywords=["pylint", "airflow", "plugin"],
    extras_require={"ci": ci},
)
