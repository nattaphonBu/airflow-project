import os
from unittest import TestCase

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.models import DagBag


class CreateCallTrackingUsagePipeline(TestCase):
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = self.dagbag.get_dag('create_call_tracking_usage_pipeline')
        self.dag_login_aws = self.dag_id.tasks[0]
        self.dag_create_call_tracking_usage = self.dag_id.tasks[1]

    def test_dag_login_aws_should_see_task_id(self):
        actual = self.dag_login_aws.task_id

        expected = 'login_aws'
        self.assertEqual(actual, expected)

    def test_dag_login_aws_should_see_bash_command(self):
        actual = self.dag_login_aws.bash_command

        expected = '$(aws ecr get-login --region eu-west-1 --no-include-email)'
        self.assertEqual(actual, expected)

    def test_dag_create_call_tracking_usage_should_see_task_id(self):
        actual = self.dag_create_call_tracking_usage.task_id

        expected = 'create_call_tracking_usage_pipeline'
        self.assertEqual(actual, expected)
    
    def test_dag_create_call_tracking_usage_should_see_auto_remove(self):
        actual = self.dag_create_call_tracking_usage.auto_remove

        self.assertTrue(actual)

    def test_dag_create_call_tracking_usage_should_see_image(self):
        actual = self.dag_create_call_tracking_usage.image

        expected = '133506877714.dkr.ecr.eu-west-1.amazonaws.com/pronto-dashboard'
        self.assertIn(expected, actual)

    def test_dag_create_call_tracking_usage_see_command(self):
        actual = self.dag_create_call_tracking_usage.command

        expected = 'python pronto_dashboard/manage.py create_call_tracking_usage --settings=pronto_dashboard.settings'
        self.assertIn(expected, actual)