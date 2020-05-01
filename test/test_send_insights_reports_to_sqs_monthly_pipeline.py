import os
from unittest import TestCase
from unittest.mock import patch

from airflow import DAG
from airflow.exceptions import AirflowException
from airflow.models import DagBag


class SendInsightsReportsToSqsMonthlyPipelineTest(TestCase):
    def setUp(self):
        self.dagbag = DagBag()
        self.dag_id = self.dagbag.get_dag('send_insights_reports_to_sqs_monthly_pipeline')
        self.dag_login_aws = self.dag_id.tasks[0]
        self.dag_send_insights_reports_to_sqs_monthly_pipeline = self.dag_id.tasks[1]

    def test_dag_login_aws_should_see_task_id(self):
        actual = self.dag_login_aws.task_id

        expected = 'login_aws'
        self.assertEqual(actual, expected)
    
    def test_dag_login_aws_should_see_bash_command(self):
        actual = self.dag_login_aws.bash_command
        
        expected = '$(aws ecr get-login --region eu-west-1 --no-include-email)'
        self.assertEqual(actual, expected)

    def test_dag_send_insights_reports_to_sqs_monthly_pipeline_pipeline_should_see_task_id(self):
        actual = self.dag_send_insights_reports_to_sqs_monthly_pipeline.task_id

        expected = 'send_insights_reports_to_sqs_monthly_pipeline'
        self.assertEqual(actual, expected)

    @patch.dict('os.environ', { 'DATABASE_HOST': '192.68.33.61',
            'ELASTICSEARCH_URL': 'http://192.68.33.61:9200',
            'DYNAMODB_HOST': 'http://192.68.33.61:4567', })
    def test_dag_send_insights_reports_to_sqs_monthly_pipeline_should_see_environment(self):
        expected = {
            'DATABASE_HOST': '192.68.33.61',
            'ELASTICSEARCH_URL': 'http://192.68.33.61:9200',
            'DYNAMODB_HOST': 'http://192.68.33.61:4567',
        } 
        self.assertEqual(os.environ['DATABASE_HOST'], expected.get('DATABASE_HOST'))
        self.assertEqual(os.environ['ELASTICSEARCH_URL'], expected.get('ELASTICSEARCH_URL'))
        self.assertEqual(os.environ['DYNAMODB_HOST'], expected.get('DYNAMODB_HOST'))
        
    def test_dag_send_insights_reports_to_sqs_monthly_pipeline_should_see_auto_remove(self):
        actual = self.dag_send_insights_reports_to_sqs_monthly_pipeline.auto_remove

        expected = True
        self.assertEqual(actual, expected)

    def test_dag_send_insights_reports_to_sqs_monthly_pipeline_should_see_image(self):
        actual = self.dag_send_insights_reports_to_sqs_monthly_pipeline.image

        expected = '133506877714.dkr.ecr.eu-west-1.amazonaws.com/pronto-dashboard'
        self.assertIn(expected, actual)

    def test_dag_send_insights_reports_to_sqs_monthly_pipeline_should_see_command(self):
        actual = self.dag_send_insights_reports_to_sqs_monthly_pipeline.command

        expected = 'python pronto_dashboard/manage.py send_insights_reports_to_sqs -c monthly --settings=pronto_dashboard.settings'
        self.assertIn(expected, actual)