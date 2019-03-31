# [match-dagid-filename]
"""DAG assignment via context manager, checking airflow.models.DAG()"""

import airflow.models

with airflow.models.DAG(dag_id="foobar") as dag:
    pass
