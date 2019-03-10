"""
This script fetches all messages from the Pylint-Airflow plugin and writes into a
Markdown table, to be copied into README.md.

Made a custom script because I wanted messages ordered by
1. pylint message type (I, C, R, W, E, F) and
2. message code

For example:
| Code  | Symbol  | Description |
|-------|---------|-------------|
| C8300 | symbol1 | Lorem ipsum |
| C8301 | symbol2 | Lorem ipsum |
| R8300 | symbol3 | Lorem ipsum |
| E8300 | symbol3 | Lorem ipsum |
| E8301 | symbol3 | Lorem ipsum |
"""

from collections import defaultdict

from pylint.lint import PyLinter

from pylint_airflow.checkers import register_checkers


def is_class_part_of_pylint_airflow(class_):
    """Expected input e.g. <class 'pylint_airflow.checkers.operator.OperatorChecker'>"""
    return class_.__module__.split(".")[0] == "pylint_airflow"


# Collect all pylint_airflow messages
# Store messages as {"type": {"msgid numbers": (symbol, description)}} for easy sorting
# E.g. {'E': {'8300': ('duplicate-dag-name', 'DAG name should be unique.')}}
messages = defaultdict(dict)
max_symbol_length = len("Symbol")
max_description_length = len("Description")
linter = PyLinter()
register_checkers(linter)
for message in linter.msgs_store.messages:
    if is_class_part_of_pylint_airflow(message.checker):
        messages[message.msgid[0]][message.msgid[-4:]] = (message.symbol, message.descr)

        if len(message.symbol) > max_symbol_length:
            max_symbol_length = len(message.symbol)
        if len(message.descr) > max_description_length:
            max_description_length = len(message.descr)

# Generate Markdown table
result = f"""\
| Code  | {"Symbol".ljust(max_symbol_length)} | {"Description".ljust(max_description_length)} |
|-------|{"-" * (max_symbol_length + 2)}|{"-" * (max_description_length + 2)}|\n"""

pylint_message_order = ["I", "C", "R", "W", "E", "F"]
for msgid_char, char_msgs in sorted(
    messages.items(), key=lambda i: pylint_message_order.index(i[0])
):
    for msgid_nums, msg in sorted(char_msgs.items()):
        result += (
            f"| {msgid_char}{msgid_nums} | "
            f"{msg[0].ljust(max_symbol_length)} | "
            f"{msg[1].ljust(max_description_length)} |\n"
        )

print(
    "{color_red}Copy the following into README.md:{no_color}\n".format(
        color_red="\x1b[1;31;40m", no_color="\x1b[0m"
    )
)
print(result)
