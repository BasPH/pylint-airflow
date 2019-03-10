import astroid
from pylint.testutils import CheckerTestCase, Message

import pylint_airflow


class TestXComChecker(CheckerTestCase):
    CHECKER_CLASS = pylint_airflow.checkers.xcom.XComChecker

    def test_used_xcom(self):
        testcase = """
        from airflow.operators.python_operator import PythonOperator
        
        def _pushtask():
            print("do stuff")
            return "foobar"
        
        pushtask = PythonOperator(task_id="pushtask", python_callable=_pushtask)
            
        def _pulltask(task_instance, **_):
            print(task_instance.xcom_pull(task_ids="pushtask"))
            
        pulltask = PythonOperator(task_id="pulltask", python_callable=_pulltask, provide_context=True)
        """
        ast = astroid.parse(testcase)
        with self.assertNoMessages():
            self.checker.visit_module(ast)

    def test_unused_xcom(self):
        testcase = """
        from airflow.operators.python_operator import PythonOperator

        def _pushtask():
            print("do stuff")
            return "foobar"

        pushtask = PythonOperator(task_id="pushtask", python_callable=_pushtask)

        def _pulltask():
            print("foobar")

        pulltask = PythonOperator(task_id="pulltask", python_callable=_pulltask)
        """
        ast = astroid.parse(testcase)
        expected_msg_node = ast.body[2].value
        expected_args = "_pushtask"
        with self.assertAddsMessages(
            Message(msg_id="unused-xcom", node=expected_msg_node, args=expected_args)
        ):
            self.checker.visit_module(ast)
