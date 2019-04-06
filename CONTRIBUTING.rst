############
Contributing
############

Ideas and contributions are always welcome! Please create an issue or PR on `GitHub <https://github.com/BasPH/pylint-airflow>`_.

**********
Tools used
**********

- `Black <https://github.com/ambv/black>`_ for formatting
- `Pylint <https://www.pylint.org>`_ for linting
- `Pytest <https://pytest.org>`_ for testing
- `Read the Docs <https://readthedocs.org>`_ for hosting the documentation
- `Sphinx <http://www.sphinx-doc.org>`_ for documentation
- `CircleCI <https://circleci.com>`_ for CI/CD

********
Makefile
********

The project contains a Makefile with a few commonly used targets. The Makefile and CircleCI should align so that you can run the full CI pipeline locally with just `make ci`. Other useful targets are (check the Makefile for all targets):

- ``make black``: check Black formatting
- ``make pylint``: check Pylint
- ``make pytest``: run all tests
- ``make validate_message_ids``: check if messages are defined without gaps between ID numbers

***************
Adding messages
***************
- Check the README for existing messages and add your new message with type and highest ID + 1.
- To generate the table in the README, run ``python scripts/generate_codes_table.py`` and copy-paste in the README.rst.
- The CI checks if message IDs are defined and increment by 1, without gaps.
- Always add tests.
- Run CI pipeline locally with ``make ci``.

***********
Conventions
***********
- Line length is set to 100 characters in .pylintrc and Makefile black target.
- Documentation is written in reStructuredText (rst) format.
- Versioning according to SemVer versioning (Read the Docs parses git tags against `PEP 440 <https://www.python.org/dev/peps/pep-0440>`_ rules to version the documentation).
- Checkers are organized by Airflow component (DAG, Operator, Hook, etc).

***************
Getting started
***************
If you're using PyCharm/IntelliJ, mark the ``src`` directory as "Sources Root". That way pylint-airflow is recognised as the local application, and "Optimize imports" groups those imports correctly.

Some pointers if you're new to Pylint plugin development:

- Check AST tokens on any script by running on the terminal:

.. code-block:: python

    import astroid
    print(astroid.parse('''your script here''').repr_tree())

    # For example:
    print(astroid.parse('''test = "foobar"''').repr_tree())

    Module(
       name='',
       doc=None,
       file='<?>',
       path=['<?>'],
       package=False,
       pure_python=True,
       future_imports=set(),
       body=[Assign(
             targets=[AssignName(name='test')],
             value=Const(value='foobar'))])

- Or in a debugging session on any given AST node:

.. code-block:: python

    print(node.repr_tree())

    # For example:
    node = astroid.parse('''test = "foobar"''')
    print(node.repr_tree())

- Define ``visit_[token]`` or ``leave_[token]`` methods to process respective tokens, e.g. ``visit_module()``.
- All available token types: http://pylint.pycqa.org/projects/astroid/en/latest/api/astroid.nodes.html.
- Pylint searches for the variable ``msgs`` in a checker, make sure it is named exactly that.
- Pylint lends itself nicely for test driven development: add one or more test cases (preferably both valid and invalid cases), and then implement a checker to run the test cases successfully.
- Some useful resources to learn about Pylint:

  - `How to write Pylint plugins by Alexander Todorov - PiterPy 2018 <https://piterpy.com/system/attachments/files/000/001/519/original/how_to_write_pylint_plugins_PiterPy_2018.pdf>`_
  - `Pylint source code <https://github.com/PyCQA/pylint>`_
  - `Pylint Django plugin source code <https://github.com/PyCQA/pylint-django)>`_
