import os
from unittest import TestCase

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.models import DagBag


class UpdateSubscriptionPipelineTest(TestCase):
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = self.dagbag.get_dag('update_subscriptions_pipeline')
        self.dag_login_aws = self.dag_id.tasks[0]
        self.dag_update_subscription = self.dag_id.tasks[1]

    def test_dag_login_aws_should_see_task_id(self):
        actual = self.dag_login_aws.task_id

        expected = 'login_aws'
        self.assertEqual(actual, expected)
    
    def test_dag_login_aws_should_see_bash_command(self):
        actual = self.dag_login_aws.bash_command
        
        expected = '$(aws ecr get-login --region eu-west-1 --no-include-email)'
        self.assertEqual(actual, expected)

    def test_dag_update_subscription_pipeline_should_see_task_id(self):
        actual = self.dag_update_subscription.task_id

        expected = 'update_subscription_pipeline'
        self.assertEqual(actual, expected)

    def test_dag_update_subscription_pipeline_should_see_auto_remove(self):
        actual = self.dag_update_subscription.auto_remove

        self.assertTrue(actual)

    def test_dag_update_subscription_pipeline_should_see_image(self):
        actual = self.dag_update_subscription.image

        expected = '133506877714.dkr.ecr.eu-west-1.amazonaws.com/pronto-dashboard'
        self.assertIn(expected, actual)

    def test_dag_update_subscription_pipeline_should_see_command(self):
        actual = self.dag_update_subscription.command

        expected = 'python pronto_dashboard/manage.py update_subscriptions --settings=pronto_dashboard.settings'
        self.assertIn(expected, actual)

