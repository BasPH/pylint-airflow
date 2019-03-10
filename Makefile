.PHONY: black
black:
	find . -name '*.py' | xargs black --check --line-length=100

.PHONY: pylint
pylint:
	find . -name '*.py' | xargs pylint --output-format=colorized
