import astroid
import pytest
from pylint.testutils import CheckerTestCase, Message

import pylint_airflow


class TestOperatorChecker(CheckerTestCase):
    CHECKER_CLASS = pylint_airflow.checkers.operator.OperatorChecker

    def test_different_operator_varname_taskid(self):
        testcase = """
        from airflow.operators.dummy_operator import DummyOperator
        mytask = DummyOperator(task_id="foo") #@
        """
        expected_message = "different-operator-varname-taskid"

        assign_node = astroid.extract_node(testcase)
        with self.assertAddsMessages(Message(msg_id=expected_message, node=assign_node)):
            self.checker.visit_assign(assign_node)

    def test_different_operator_varname_taskid_baseoperator(self):
        testcase = """
        from airflow.models import BaseOperator
        mytask = BaseOperator(task_id="foo") #@
        """
        expected_message = "different-operator-varname-taskid"

        assign_node = astroid.extract_node(testcase)
        with self.assertAddsMessages(Message(msg_id=expected_message, node=assign_node)):
            self.checker.visit_assign(assign_node)

    def test_different_operator_varname_taskid_valid(self):
        testcase = """
        from airflow.operators.dummy_operator import DummyOperator
        mytask = DummyOperator(task_id="mytask") #@
        """

        assign_node = astroid.extract_node(testcase)
        with self.assertNoMessages():
            self.checker.visit_assign(assign_node)

    def test_match_callable_taskid(self):
        testcase = """
        from airflow.operators.python_operator import PythonOperator
        
        def foo():
            print("dosomething")
            
        mytask = PythonOperator(task_id="mytask", python_callable=foo) #@
        """
        expected_message = "match-callable-taskid"

        assign_node = astroid.extract_node(testcase)
        with self.assertAddsMessages(Message(msg_id=expected_message, node=assign_node)):
            self.checker.visit_assign(assign_node)

    def test_not_match_callable_taskid(self):
        testcase = """
        from airflow.operators.python_operator import PythonOperator

        def _mytask():
            print("dosomething")

        mytask = PythonOperator(task_id="mytask", python_callable=_mytask) #@
        """

        assign_node = astroid.extract_node(testcase)
        with self.assertNoMessages():
            self.checker.visit_assign(assign_node)

    @pytest.mark.parametrize(
        "dependencies,expect_msg",
        [
            ("t1 >> t2", False),
            ("t1 >> t2 >> t3 >> t4 >> t5", False),
            ("t1 >> [t2, t3]", False),
            ("[t1, t2] >> t3", False),
            ("[t1, t2] >> t3 << t4", True),
            ("t1 >> t2 << [t3, t4]", True),
            ("[t1, t2] >> t3 << [t4, t5]", True),
        ],
    )
    def test_mixed_dependency_directions(self, dependencies, expect_msg):
        testcase = f"""
        from airflow.operators.dummy_operator import DummyOperator
        t1 = DummyOperator(task_id="t1")
        t2 = DummyOperator(task_id="t2")
        t3 = DummyOperator(task_id="t3")
        t4 = DummyOperator(task_id="t4")
        t5 = DummyOperator(task_id="t5")
        {dependencies} #@
        """
        message = "mixed-dependency-directions"
        binop_node = astroid.extract_node(testcase)

        if expect_msg:
            with self.assertAddsMessages(Message(msg_id=message, node=binop_node)):
                self.checker.visit_binop(binop_node)
        else:
            with self.assertNoMessages():
                self.checker.visit_binop(binop_node)
