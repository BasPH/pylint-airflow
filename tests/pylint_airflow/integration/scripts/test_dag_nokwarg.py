# [match-dagid-filename]
# pylint: disable=invalid-name
"""Explicit DAG assignment, checking DAG(), passing dag_id via non-keyword arg."""

from airflow.models import DAG

dag = DAG("foobar")
