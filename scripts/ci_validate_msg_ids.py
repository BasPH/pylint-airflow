"""
This script is used by the CI to:
1. Validate if message ids are defined correctly (e.g. missed comma might evaluate correctly, but
   will be interpreted incorrectly).
2. For each message type, check if codes start at 0 and increment by 1, e.g. C8300, C8301, ...
"""

from collections import defaultdict

from pylint.lint import PyLinter

from pylint_airflow.__pkginfo__ import BASE_ID
from pylint_airflow.checkers import register_checkers


def is_class_part_of_pylint_airflow(class_):
    """Expected input e.g. <class 'pylint_airflow.checkers.operator.OperatorChecker'>"""
    return class_.__module__.split(".")[0] == "pylint_airflow"


# Construct dict of {message type: [message ids]}
messages = defaultdict(list)
linter = PyLinter()
register_checkers(linter)
# Running register_checkers automatically validates there are no duplicate message ids
for message in linter.msgs_store.messages:
    if is_class_part_of_pylint_airflow(message.checker):
        message_type = message.msgid[0]
        messages[message_type].append(message.msgid)

for message_type, message_ids in messages.items():
    ids = sorted([int(msg_id[3:5]) for msg_id in message_ids])
    # ids should start at 0, should be sorted, and should be incremented by 1.
    # So with e.g. 5 ids, the last id should be 4.
    maxid = len(ids) - 1
    if ids[-1] != maxid:
        # Could come up with some sorting function for message_ids, but this proved easier
        formatted_message_ids = [f"{message_type}{BASE_ID}{str(id_).zfill(2)}" for id_ in ids]
        raise AssertionError(f"Message ids should increment by 1. {formatted_message_ids}")
