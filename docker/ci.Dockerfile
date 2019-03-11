# Used miniconda3 base image and not python because Airflow requires
# Pandas which requires Numpy which requires GCC etc...

FROM continuumio/miniconda3:4.5.12

WORKDIR /pylint-airflow
COPY scripts scripts/
COPY src/pylint_airflow src/pylint_airflow/
COPY tests tests/
COPY .pylintrc .pylintrc
COPY Makefile Makefile
COPY setup.py setup.py

RUN apt update && \
	apt install -y gcc g++ --no-install-recommends && \
    # As long as Airflow requires this GPL dependency we have to install with SLUGIFY_USES_TEXT_UNIDECODE=yes
    # https://github.com/apache/airflow/pull/4513
    SLUGIFY_USES_TEXT_UNIDECODE=yes pip install .[ci] && \
	apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*
