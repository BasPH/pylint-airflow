# [match-dagid-filename]
"""DAG assignment via context manager, checking models.DAG()"""

from airflow import models

with models.DAG(dag_id="foobar") as dag:
    pass
