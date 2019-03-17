.PHONY: black
black:
	find . -name '*.py' | xargs black --check --line-length=100

.PHONY: pylint
pylint:
	find . -name '*.py' | xargs pylint --output-format=colorized

.PHONY: validate_message_ids
validate_message_ids:
	python scripts/ci_validate_msg_ids.py

.PHONY: pytest
pytest:
	pytest tests/ -W ignore::DeprecationWarning

.PHONY: clean-compiled
clean-compiled:  # Remove Python artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

.PHONY: ci
ci: | clean-compiled black pylint validate_message_ids pytest

.PHONY: ci-docker
ci-docker: build_ci_image
	docker run basph/pylint-airflow-ci:3.6
	docker run basph/pylint-airflow-ci:3.7

.PHONY: build_ci_image
build_ci_image:
	docker build --file docker/ci.Dockerfile --build-arg CONDA_PYTHON_VERSION=3.6 --tag basph/pylint-airflow-ci:3.6 .
	docker build --file docker/ci.Dockerfile --build-arg CONDA_PYTHON_VERSION=3.7 --tag basph/pylint-airflow-ci:3.7 .
