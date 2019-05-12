"""Checks on Airflow XComs."""

import astroid
from pylint import checkers
from pylint import interfaces
from pylint.checkers import utils

from pylint_airflow.__pkginfo__ import BASE_ID


class XComChecker(checkers.BaseChecker):
    """Checks on Airflow XComs."""

    __implements__ = interfaces.IAstroidChecker

    msgs = {
        f"R{BASE_ID}00": (
            "Return value from %s is stored as XCom but not used anywhere",
            "unused-xcom",
            "Return values from a python_callable function or execute() method are "
            "automatically pushed as XCom.",
        )
    }

    @utils.check_messages("unused-xcom")
    def visit_module(self, node: astroid.Module):
        """
        Check for unused XComs.
        XComs can be set (pushed) implicitly via return of a python_callable or
        execute() of an operator. And explicitly by calling xcom_push().

        Currently this only checks unused XComs from return value of a python_callable.
        """
        # pylint: disable=too-many-locals,too-many-branches,too-many-nested-blocks
        assign_nodes = [n for n in node.body if isinstance(n, astroid.Assign)]
        call_nodes = [n.value for n in assign_nodes if isinstance(n.value, astroid.Call)]

        # Store nodes containing python_callable arg as:
        # {task_id: (call node, python_callable func name)}
        python_callable_nodes = dict()
        for call_node in call_nodes:
            if call_node.keywords:
                task_id = ""
                python_callable = ""
                for keyword in call_node.keywords:
                    if keyword.arg == "python_callable":
                        python_callable = keyword.value.name
                        continue
                    elif keyword.arg == "task_id":
                        task_id = keyword.value.value

                if python_callable:
                    python_callable_nodes[task_id] = (call_node, python_callable)

        # Now fetch the functions mentioned by python_callable args
        xcoms_pushed = dict()
        xcoms_pulled_taskids = set()
        for (task_id, (python_callable, callable_func_name)) in python_callable_nodes.items():
            if callable_func_name != "<lambda>":
                # TODO support lambdas
                callable_func = node.getattr(callable_func_name)[0]

                if isinstance(callable_func, astroid.FunctionDef):
                    # Callable_func is str not FunctionDef when imported
                    callable_func = node.getattr(callable_func_name)[0]

                    # Check if the function returns any values
                    if any([isinstance(n, astroid.Return) for n in callable_func.body]):
                        # Found a return statement
                        xcoms_pushed[task_id] = (python_callable, callable_func_name)

                    # Check if the function pulls any XComs
                    callable_func_calls = callable_func.nodes_of_class(astroid.Call)
                    for callable_func_call in callable_func_calls:
                        if (
                            isinstance(callable_func_call.func, astroid.Attribute)
                            and callable_func_call.func.attrname == "xcom_pull"
                        ):
                            for keyword in callable_func_call.keywords:
                                if keyword.arg == "task_ids":
                                    xcoms_pulled_taskids.add(keyword.value.value)

        remainder = xcoms_pushed.keys() - xcoms_pulled_taskids
        if remainder:
            # There's a remainder in xcoms_pushed_taskids which should've been xcom_pulled.
            for remainder_task_id in remainder:
                python_callable, callable_func_name = xcoms_pushed[remainder_task_id]
                self.add_message("unused-xcom", node=python_callable, args=callable_func_name)

        # pylint: enable=too-many-locals,too-many-branches,too-many-nested-blocks
