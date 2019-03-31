# [match-dagid-filename]
"""Explicit DAG assignment, checking airflow.models.DAG()"""
# pylint: disable=invalid-name

import airflow.models

dag = airflow.models.DAG(dag_id="foobar")
