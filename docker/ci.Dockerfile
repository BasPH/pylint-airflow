# Used miniconda3 base image and not python because Airflow requires
# Pandas which requires Numpy which requires GCC etc...

FROM continuumio/miniconda3:4.5.12

ARG CONDA_PYTHON_VERSION

WORKDIR /pylint-airflow
# Note: only copy requirements.txt which contains development dependencies. The repository should
# be mounted to the container at runtime.
COPY requirements.txt requirements.txt

# As long as Airflow requires this GPL dependency we have to install with SLUGIFY_USES_TEXT_UNIDECODE=yes
# https://github.com/apache/airflow/pull/4513
RUN	conda install --yes python=${CONDA_PYTHON_VERSION} && \
    apt-get update && \
	apt-get install -y gcc g++ make --no-install-recommends && \
	SLUGIFY_USES_TEXT_UNIDECODE=yes pip install -r requirements.txt && \
	apt-get remove -y --purge gcc g++ && \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

# Note: In CircleCI if no command is specified then command and entrypoint are be ignored. See https://circleci.com/docs/2.0/configuration-reference/#docker
# Note2: The entrypoint script is not built into the image! It must be volume mounted to a running container.
ENTRYPOINT ["./docker/entrypoint.sh"]
