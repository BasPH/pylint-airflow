# [match-dagid-filename]
"""Explicit DAG assignment, checking models.DAG()"""
# pylint: disable=invalid-name

from airflow import models

dag = models.DAG(dag_id="foobar")
