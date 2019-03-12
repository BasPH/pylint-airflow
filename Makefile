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
	pytest tests/

.PHONY: ci
ci: | black pylint validate_message_ids pytest

.PHONY: build_ci_image
build_ci_image:
	docker build -f docker/ci.Dockerfile .
