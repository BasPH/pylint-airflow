"""DAG assignment via context manager, checking DAG()"""

from airflow.models import DAG

with DAG(dag_id="foobar") as dag:
    pass
