"""
This script fetches all messages from the Pylint-Airflow plugin and writes into a
Markdown table, to be copied into README.rst.

Made a custom script because I wanted messages ordered by
1. pylint message type (I, C, R, W, E, F) and
2. message code

For example:
+-------+---------+-------------+
| Code  | Symbol  | Description |
+=======+=========+=============+
| C8300 | symbol1 | Lorem ipsum |
+-------+---------+-------------+
| C8301 | symbol2 | Lorem ipsum |
+-------+---------+-------------+
| R8300 | symbol3 | Lorem ipsum |
+-------+---------+-------------+
| E8300 | symbol3 | Lorem ipsum |
+-------+---------+-------------+
| E8301 | symbol3 | Lorem ipsum |
+-------+---------+-------------+
"""

from collections import defaultdict
from typing import List, Dict, Tuple

from pylint.lint import PyLinter

from pylint_airflow.checkers import register_checkers


def is_class_part_of_pylint_airflow(class_):
    """Expected input e.g. <class 'pylint_airflow.checkers.operator.OperatorChecker'>"""
    return class_.__module__.split(".")[0] == "pylint_airflow"


def gen_splitter(symbol: str, lengths: List[int]):
    """
    Generate a "splitter" line for an rst table.
    E.g. +-------+---------+-------------+
    :param str symbol: The character to use for filling cells
    :param List[int] lengths: The length of each cell to generate
    :return: Splitter line
    :rtype: str
    """

    content = f"{symbol}+{symbol}".join(f"{symbol*nchars}" for nchars in lengths)
    return f"+{symbol}{content}{symbol}+"


def gen_single_row(content: List, lengths: List[int]):
    """
    Generate a row for an rst table.
    E.g. "| C8300 | symbol1 | Lorem ipsum |"
    :param List content: The values of each cell
    :param List[int] lengths: The length of each cell to generate
    :return: Table row with whitespace padded cells
    :rtype: str
    """
    assert len(content) == len(lengths)
    content_length = list(zip(content, lengths))
    row = " | ".join(f"{value.ljust(length)}" for value, length in content_length)
    return f"| {row} |"


def gen_content(msgs: Dict[str, Dict[str, Tuple[str, str]]], lengths: List[int]):
    """
    Generate the content part of an rst table.
    :param Dict[str, Dict[str, Tuple[str, str]]] msgs: all values for the table
        ({msg type: {msg number: (symbol, description)}})
    :param List[int] lengths: The length of each cell to generate
    :return: Formatted table rows
    :rtype: str
    """
    lines = []
    splitter = gen_splitter(symbol="-", lengths=lengths)

    pylint_message_order = ["I", "C", "R", "W", "E", "F"]
    for msgid_char, char_msgs in sorted(
        msgs.items(), key=lambda i: pylint_message_order.index(i[0])
    ):
        for msgid_nums, msg in sorted(char_msgs.items()):
            content = [msgid_char + msgid_nums, msg[0], msg[1]]
            lines.append(gen_single_row(content=content, lengths=lengths))

    return f"\n{splitter}\n".join(lines)


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
col_lengths = [5, max_symbol_length, max_description_length]
table = [
    gen_splitter(symbol="-", lengths=col_lengths),
    gen_single_row(content=["Code", "Symbol", "Description"], lengths=col_lengths),
    gen_splitter(symbol="=", lengths=col_lengths),
    gen_content(msgs=messages, lengths=col_lengths),
    gen_splitter(symbol="-", lengths=col_lengths),
]
result = "\n".join(table)

print(
    "{color_red}Copy the following into README.rst:{no_color}\n".format(
        color_red="\x1b[1;31;40m", no_color="\x1b[0m"
    )
)
print(result)
