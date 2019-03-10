"""Checks on Airflow operators."""

import astroid
from pylint import checkers
from pylint import interfaces
from pylint.checkers import utils
from pylint.checkers.utils import safe_infer

from pylint_airflow.__pkginfo__ import BASE_ID


class OperatorChecker(checkers.BaseChecker):
    """Checks on Airflow operators."""

    __implements__ = (interfaces.IAstroidChecker,)

    msgs = {
        f"C{BASE_ID}00": (
            "Operator variable name and task_id argument should match",
            "different-operator-varname-taskid",
            "For consistency assign the same variable name and task_id to operators.",
        ),
        f"C{BASE_ID}01": (
            "Name the python_callable function '_[task_id]'",
            "match-callable-taskid",
            "For consistency name the callable function '_[task_id]', e.g. "
            "PythonOperator(task_id='mytask', python_callable=_mytask).",
        ),
        f"C{BASE_ID}02": (
            "Avoid mixing task dependency directions",
            "mixed-dependency-directions",
            "For consistency don't mix directions in a single statement, instead split "
            "over multiple statements.",
        ),
        f"C{BASE_ID}03": (
            "Task {} has no dependencies. Verify or disable message.",
            "task-no-dependencies",
            "Sometimes a task without any dependency is desired, however often it is "
            "the result of a forgotten dependency.",
        ),
    }

    # @utils.check_messages("different-operator-varname-taskid")
    # def visit_assign(self, node):
    #     """
    #     Check if variable name equals operator task_id.
    #     Does not apply to operators defined in a list comprehension.
    #     For example:
    #     Valid       -> mytask = DummyOperator(task_id="mytask", ...)
    #     Invalid     -> mytask = DummyOperator(task_id="something_else", ...)
    #     Not checked -> multi = [DummyOperator(task_id=f"t_{i}", ...) for i in range(5)]
    #     """
    #     if isinstance(node.value, astroid.Call):
    #         function_node = safe_infer(node.value.func)
    #         if "BaseOperator" in [base.name for base in function_node.bases]:
    #             # Now we know this assignment is an Airflow operator
    #             # TODO check if this thing is a BaseOperator itself
    #             var_name = node.targets[0].name
    #             for keyword in node.value.keywords:
    #                 if keyword.arg == "task_id":
    #                     task_id = keyword.value.value
    #                     if var_name != task_id:
    #                         self.add_message(
    #                             "different-operator-varname-taskid", node=node
    #                         )

    @utils.check_messages("match-callable-taskid")
    def visit_assign(self, node):
        """
        Check if operators using python_callable argument call a function with name
        '_[task_id]'. For example:
        Valid ->
        def _mytask(): print("dosomething")
        mytask = PythonOperator(task_id="mytask", python_callable=_mytask)

        Invalid ->
        def invalidname(): print("dosomething")
        mytask = PythonOperator(task_id="mytask", python_callable=invalidname)
        """
        if isinstance(node.value, astroid.Call):
            function_node = safe_infer(node.value.func)
            if "BaseOperator" in [base.name for base in function_node.bases]:
                # Now we know this assignment is an Airflow operator
                # TODO check if this thing is a BaseOperator itself
                task_id = None
                python_callable_name = None

                for keyword in node.value.keywords:
                    if keyword.arg == "task_id":
                        task_id = keyword.value
                    elif keyword.arg == "python_callable":
                        python_callable_name = keyword.value

                if python_callable_name and f"_{task_id}" != python_callable_name:
                    self.add_message("match-callable-taskid", node=node)

    @utils.check_messages("mixed-dependency-directions")
    def visit_expr(self, node):
        """
        Check if bitshift operator directions for setting dependencies are mixed.
        Valid   -> t1 >> t2 >> t3
        Invalid -> t1 >> t2 << t3
        """
        if isinstance(node.value, astroid.BinOp):

            def fetch_binops(node):
                """
                Method fetching binary operations (>> and/or <<).
                Resides in separate function for recursion.
                """
                binops_found = set()
                if hasattr(node, "value"):
                    if isinstance(node.value.left, astroid.BinOp):
                        binops_found.update(fetch_binops(node.value.left))
                    if isinstance(node.value.right, astroid.BinOp):
                        binops_found.update(fetch_binops(node.value.right))

                    if node.value.op == ">>" or node.value.op == "<<":
                        binops_found.add(node.value.op)
                else:
                    if node.op == ">>" or node.op == "<<":
                        binops_found.add(node.op)

                return binops_found

            binops = fetch_binops(node)
            if ">>" in binops and "<<" in binops:
                self.add_message("mixed-dependency-directions", node=node)
