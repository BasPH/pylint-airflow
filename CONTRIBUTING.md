# Contributing

Ideas and contributions are always welcome! Please create an issue or PR on [GitHub](https://github.com/BasPH/pylint-airflow).

## Tools used

- [Black](https://github.com/ambv/black) for formatting
- [Pylint](https://www.pylint.org) for linting
- [Pytest](https://pytest.org) for testing
- [Read the Docs](https://readthedocs.org) for hosting the documentation
- [Sphinx](http://www.sphinx-doc.org) for documentation

## Adding messages
The README.md shows a Markdown table with all messages in this plugin. To generate the table, run `python scripts/generate_codes_table.py` and copy-paste in the README.md.

## Conventions
- Line length is set to 100 characters in .pylintrc and Makefile black target.
- Documentation is written in reStructuredText (rst) format.

## Getting started
Some pointers if you're new to Pylint plugin development:
- Check AST tokens on any script by running on the terminal:

```python
import astroid
print(astroid.parse('''your script here''').repr_tree())
```

- Define `visit_[token]` or `leave_[token]` methods to process respective tokens.
- All available token types: http://pylint.pycqa.org/projects/astroid/en/latest/api/astroid.nodes.html.
- Some useful resources to learn about Pylint:
    - [How to write Pylint plugins by Alexander Todorov - PiterPy 2018](https://piterpy.com/system/attachments/files/000/001/519/original/how_to_write_pylint_plugins_PiterPy_2018.pdf)
