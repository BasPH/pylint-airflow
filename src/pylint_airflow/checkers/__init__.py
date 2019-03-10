"""Checkers"""

from pylint_airflow.checkers.dag import DagChecker
from pylint_airflow.checkers.operator import OperatorChecker
from pylint_airflow.checkers.xcom import XComChecker


def register_checkers(linter):
    """Register checkers."""
    linter.register_checker(DagChecker(linter))
    linter.register_checker(OperatorChecker(linter))
    linter.register_checker(XComChecker(linter))
