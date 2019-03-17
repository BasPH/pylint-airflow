# Used miniconda3 base image and not python because Airflow requires
# Pandas which requires Numpy which requires GCC etc...

FROM continuumio/miniconda3:4.5.12

WORKDIR /pylint-airflow
# Note: Items to exclude in the Docker image are listed in .dockerignore
COPY . .

# As long as Airflow requires this GPL dependency we have to install with SLUGIFY_USES_TEXT_UNIDECODE=yes
# https://github.com/apache/airflow/pull/4513
RUN apt-get update && \
	apt-get install -y gcc g++ make --no-install-recommends && \
	SLUGIFY_USES_TEXT_UNIDECODE=yes pip install .[dev] && \
	apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

CMD ["make", "ci"]
