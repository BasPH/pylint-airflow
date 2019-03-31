"""Checks on Airflow DAGs."""

from collections import defaultdict

import astroid
from pylint import checkers
from pylint import interfaces
from pylint.checkers import utils
from pylint.checkers.utils import safe_infer

from pylint_airflow.__pkginfo__ import BASE_ID


class DagChecker(checkers.BaseChecker):
    """Checks conditions in the context of (a) complete DAG(s)."""

    __implements__ = interfaces.IAstroidChecker

    msgs = {
        f"W{BASE_ID}00": (
            "Don't place BaseHook calls at the top level of DAG script",
            "basehook-top-level",
            "Airflow executes DAG scripts periodically and anything at the top level "
            "of a script is executed. Therefore, move BaseHook calls into "
            "functions/hooks/operators.",
        ),
        f"E{BASE_ID}00": (
            "DAG name %s already used",
            "duplicate-dag-name",
            "DAG name should be unique.",
        ),
        f"E{BASE_ID}01": (
            "Task name {} already used",
            "duplicate-task-name",
            "Task name within a DAG should be unique.",
        ),
        f"E{BASE_ID}02": (
            "Task dependency {}->{} already set",
            "duplicate-dependency",
            "Task dependencies can be defined only once.",
        ),
        f"E{BASE_ID}03": (
            "DAG {} contains cycles",
            "dag-with-cycles",
            "A DAG is acyclic and cannot contain cycles.",
        ),
        f"E{BASE_ID}04": (
            "Task {} is not bound to any DAG instance",
            "task-no-dag",
            "A task must know a DAG instance to run.",
        ),
        f"C{BASE_ID}06": (
            "For consistency match the DAG filename with the dag_id",
            "match-dagid-filename",
            "For consistency match the DAG filename with the dag_id.",
        ),
    }

    @utils.check_messages("duplicate-dag-name", "match-dagid-filename")
    def visit_module(self, node: astroid.Module):
        """Checks in the context of (a) complete DAG(s)."""
        dagids_nodes = defaultdict(list)
        assigns = node.nodes_of_class(astroid.Assign)
        withs = node.nodes_of_class(astroid.With)

        # Find DAGs in assignments
        for assign in assigns:
            if isinstance(assign.value, astroid.Call):
                func = assign.value.func
                if (hasattr(func, "name") and func.name == "DAG") or (
                    hasattr(func, "attrname") and func.attrname == "DAG"
                ):
                    function_node = safe_infer(func)
                    if function_node.is_subtype_of("airflow.models.DAG"):
                        for keyword in assign.value.keywords:
                            # Currently only constants supported
                            if keyword.arg == "dag_id" and isinstance(keyword.value, astroid.Const):
                                dagids_nodes[keyword.value.value].append(assign)

        # Find DAGs in context managers
        for with_ in withs:
            for with_item in with_.items[0]:
                if isinstance(with_item, astroid.Call):
                    func = with_item.func
                    if (hasattr(func, "name") and func.name == "DAG") or (
                        hasattr(func, "attrname") and func.attrname == "DAG"
                    ):
                        function_node = safe_infer(func)
                        if function_node.is_subtype_of("airflow.models.DAG"):
                            for keyword in with_item.keywords:
                                if keyword.arg == "dag_id" and isinstance(
                                    keyword.value, astroid.Const
                                ):
                                    dagids_nodes[keyword.value.value].append(with_item)

        # Check if single DAG and if equals filename
        # Unit test nodes have file "<?>"
        if len(dagids_nodes) == 1 and node.file != "<?>":
            dagid, _ = list(dagids_nodes.items())[0]
            expected_filename = f"{dagid}.py"
            current_filename = node.file.split("/")[-1]
            if expected_filename != current_filename:
                self.add_message("match-dagid-filename", node=node)

        duplicate_dagids = [
            (dagid, nodes) for dagid, nodes in dagids_nodes.items() if len(nodes) >= 2
        ]
        for (dagid, assign_nodes) in duplicate_dagids:
            self.add_message("duplicate-dag-name", node=assign_nodes[-1], args=dagid)
