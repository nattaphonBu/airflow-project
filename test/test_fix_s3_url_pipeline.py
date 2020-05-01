import os
from unittest import TestCase

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.models import DagBag


class TestFixS3UrlPipeline(TestCase):
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = self.dagbag.get_dag('fix_s3_recording_url_pipeline')
        self.dag_login_aws = self.dag_id.tasks[0]
        self.dag_fix_s3_recording_url = self.dag_id.tasks[1]

    def test_dag_login_aws_should_see_task_id(self):
        actual = self.dag_login_aws.task_id

        expected = 'login_aws'
        self.assertEqual(actual, expected)

    def test_dag_login_aws_should_see_bash_command(self):
        actual = self.dag_login_aws.bash_command

        expected = '$(aws ecr get-login --region eu-west-1 --no-include-email)'
        self.assertEqual(actual, expected)

    def test_dag_fix_s3_recording_url_should_see_task_id(self):
        actual = self.dag_fix_s3_recording_url.task_id

        expected = 'fix_s3_recording_url_pipeline'
        self.assertEqual(actual, expected)
    
    def test_dag_fix_s3_recording_url_should_see_auto_remove(self):
        actual = self.dag_fix_s3_recording_url.auto_remove

        self.assertTrue(actual)

    def test_dag_fix_s3_recording_url_should_see_image(self):
        actual = self.dag_fix_s3_recording_url.image

        expected = '133506877714.dkr.ecr.eu-west-1.amazonaws.com/pronto-dashboard'
        self.assertIn(expected, actual)

    def test_dag_fix_s3_recording_url_see_command(self):
        actual = self.dag_fix_s3_recording_url.command

        expected = 'python pronto_dashboard/manage.py fix_s3_recording_url --settings=pronto_dashboard.settings'
        self.assertIn(expected, actual)