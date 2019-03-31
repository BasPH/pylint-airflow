"""Mixed DAG assignment, explicit and via context manager, checking DAG()"""
# pylint: disable=invalid-name

from airflow.models import DAG

dag1 = DAG(dag_id="foobar")
with DAG(dag_id="foobar2") as dag2:
    pass
