"""Tests for the DAG checker."""
import os
import pathlib

import astroid
import pytest
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

    match_dagid_filename_testfilesdir = os.path.join(
        pytest.helpers.file_abspath(__file__), "data/test_dag/test_match_dagid_filename"
    )
    match_dagid_filename_testfiles = list(
        pathlib.Path(match_dagid_filename_testfilesdir).glob("*.py")
    )

    @pytest.mark.parametrize(
        "test_filepath",
        match_dagid_filename_testfiles,
        ids=[p.stem for p in match_dagid_filename_testfiles],
    )
    def test_match_dagid_filename(self, test_filepath):
        pytest.helpers.functional_test(test_filepath)
