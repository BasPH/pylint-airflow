.PHONY: black
black:
	find . -name '*.py' | xargs black --check --line-length=100

.PHONY: pylint
pylint:
	find . -name '*.py' | xargs pylint --output-format=colorized

.PHONY: validate_message_ids
validate_message_ids:
	python scripts/ci_validate_msg_ids.py

.PHONY: ci
ci: | black pylint validate_message_ids
