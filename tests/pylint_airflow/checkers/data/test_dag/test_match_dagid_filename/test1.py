# [match-dagid-filename]
"""Explicit DAG assignment, checking DAG()"""
# pylint: disable=invalid-name

from airflow.models import DAG

dag = DAG(dag_id="foobar")
