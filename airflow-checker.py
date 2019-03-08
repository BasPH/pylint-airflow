import astroid

from pylint import checkers
from pylint import interfaces
from pylint.checkers import utils
from pylint.checkers.utils import safe_infer


class AirflowChecker(checkers.BaseChecker):
    __implements__ = interfaces.IAstroidChecker

    name = "airflow-checker"

    msgs = {
        # R-AIR001
        "R2119": (
            "Operator variable name and task_id argument should match",
            "different-operator-varname-taskid",
            "For clarity assign the same variable name and task_id to operators.",
        ),
        "R2120": (
            "Name the python_callable function '_[task_id]'",
            "match-callable-taskid",
            "For consistency name the callable function '_[task_id]', e.g. "
            "PythonOperator(task_id='mytask', python_callable=_mytask).",
        ),
        "R2121": (
            "Avoid mixing task dependency directions",
            "mixed-dependency-directions",
            "To avoid confusion don't mix directions in a single statement, instead "
            "split over multiple statements.",
        ),
        "R2122": (
            "Don't place BaseHook calls at the top level of DAG script",
            "basehook-top-level",
            "Airflow executes DAG scripts periodically and anything at the top level "
            "of a script is executed. Therefore, move BaseHook calls into "
            "functions/hooks/operators.",
        )
        # TODO:
        # - check if top level code
        # - duplicate task ids
        # - duplicate dag ids
        # - check duplicate dependencies
        # - check cycles
        # - detect tasks without dependencies
        # - check if XComs returned by python_callable are used elsewhere
        # - check if params supplied via operator args exist
    }

    @utils.check_messages("different-operator-varname-taskid")
    def visit_assign(self, node):
        """
        Check if variable name equals operator task_id.
        Does not apply to operators defined in a list comprehension.
        For example:
        Valid       -> mytask = DummyOperator(task_id="mytask", ...)
        Invalid     -> mytask = DummyOperator(task_id="something_else", ...)
        Not checked -> multi = [DummyOperator(task_id=f"t_{i}", ...) for i in range(5)]
        """
        if isinstance(node.value, astroid.Call):
            function_node = safe_infer(node.value.func)
            if "BaseOperator" in [base.name for base in function_node.bases]:
                # Now we know this assignment is an Airflow operator
                # TODO check if this thing is a BaseOperator itself
                var_name = node.targets[0].name
                for keyword in node.value.keywords:
                    if keyword.arg == "task_id":
                        task_id = keyword.value.value
                        if var_name != task_id:
                            self.add_message(
                                "different-operator-varname-taskid", node=node
                            )

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

    def _fetch_binops(self, node):
        """Method fetching binary operations (>> and/or <<)."""
        binops_found = set()
        if hasattr(node, "value"):
            if isinstance(node.value.left, astroid.BinOp):
                binops_found.update(self._fetch_binops(node.value.left))
            if isinstance(node.value.right, astroid.BinOp):
                binops_found.update(self._fetch_binops(node.value.right))

            if node.value.op == ">>" or node.value.op == "<<":
                binops_found.add(node.value.op)
        else:
            if node.op == ">>" or node.op == "<<":
                binops_found.add(node.op)

        return binops_found

    @utils.check_messages("mixed-dependency-directions")
    def visit_expr(self, node):
        """
        Check if bitshift operator directions for setting dependencies are mixed.
        Valid   -> t1 >> t2 >> t3
        Invalid -> t1 >> t2 << t3
        """
        if isinstance(node.value, astroid.BinOp):
            binops = self._fetch_binops(node)
            if ">>" in binops and "<<" in binops:
                self.add_message("mixed-dependency-directions", node=node)


def register(linter):
    """Register this checker."""
    linter.register_checker(AirflowChecker(linter))
