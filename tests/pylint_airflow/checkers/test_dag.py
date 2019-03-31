"""Tests for the DAG checker."""

import astroid
from pylint.testutils import CheckerTestCase, Message

import pylint_airflow


class TestDagChecker(CheckerTestCase):
    """Tests for the DAG checker."""

    CHECKER_CLASS = pylint_airflow.checkers.dag.DagChecker

    def test_duplicate_dag(self):
        """Test for multiple DAG instances with identical names."""
        testcase = """
        from airflow import models
        from airflow.models import DAG
        
        dagname = "test"
        
        dag = models.DAG(dag_id="lintme")
        dag2 = DAG(dag_id="lintme")
        dag3 = DAG(dag_id=dagname)  # test dag_id from variable
        dag4 = DAG(dag_id=f"{dagname}foo")  # test dag_id as f-string
        """
        ast = astroid.parse(testcase)
        expected_msg_node = ast.body[4]
        with self.assertAddsMessages(
            Message(msg_id="duplicate-dag-name", node=expected_msg_node, args="lintme")
        ):
            self.checker.visit_module(ast)

    def test_no_duplicate_dag(self):
        """Test for multiple DAG instances without identical names - this should be fine."""
        testcase = """
        from airflow.models import DAG
        dag = DAG(dag_id="lintme")
        dag2 = DAG(dag_id="foobar")
        """
        ast = astroid.parse(testcase)
        with self.assertNoMessages():
            self.checker.visit_module(ast)
