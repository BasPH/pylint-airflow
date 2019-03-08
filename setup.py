from setuptools import setup, find_packages

setup(
    name="pylint-airflow",
    url="https://github.com/BasPH/pylint-airflow",
    description="A Pylint plugin to lint Apache Airflow code.",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["pylint"],
    keywords=["pylint", "airflow", "plugin"],
)
