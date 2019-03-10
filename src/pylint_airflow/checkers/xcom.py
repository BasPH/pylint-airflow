"""Checks on Airflow XComs."""

from pylint import checkers
from pylint import interfaces

from pylint_airflow.__pkginfo__ import BASE_ID


class XComChecker(checkers.BaseChecker):
    """Checks on Airflow XComs."""

    __implements__ = interfaces.IAstroidChecker

    msgs = {
        f"R{BASE_ID}00": (
            "Return value from {} is stored as XCom but not used anywhere",
            "unused-xcom",
            "Return values from a python_callable function or execute() method are "
            "automatically pushed as XCom.",
        )
    }
