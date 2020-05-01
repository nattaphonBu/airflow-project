import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator

from utils import send_alert_task_failure_to_slack

LOG_DIRECTORY = os.environ.get('LOG_DIRECTORY')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
DYNAMODB_HOST = os.environ.get('DYNAMODB_HOST')
IMAGE_NAME = os.environ.get('IMAGE_NAME')
ENVIRONMENT_SETTING = os.environ.get('ENVIRONMENT_SETTING')
COMMAND = 'python pronto_dashboard/manage.py remove_twilio_recordings --settings=pronto_dashboard.settings.' + ENVIRONMENT_SETTING

default_args = {
    'owner': 'ProntoTools',
    'description': 'remove twilio recording every at 01:01 on day-of-month 25',
    'depend_on_past': False,
    'start_date': datetime(2020, 1, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': send_alert_task_failure_to_slack
}

with DAG('remove_twilio_recording_pipeline', default_args=default_args, schedule_interval='1 1 25 * *', catchup=False) as dag:

    t1 = BashOperator(
        task_id='login_aws',
        bash_command='$(aws ecr get-login --region eu-west-1 --no-include-email)'
    )

    t2 = DockerOperator(
        task_id='remove_twilio_recording_pipeline',
        auto_remove=True,
        image=IMAGE_NAME,
        api_version='auto',
        command=COMMAND,
        docker_url='unix://var/run/docker.sock',
        network_mode='host',
        environment={
            'DATABASE_HOST': DATABASE_HOST,
            'ELASTICSEARCH_URL': ELASTICSEARCH_URL,
            'DYNAMODB_HOST': DYNAMODB_HOST
        },
        volumes=[LOG_DIRECTORY]
    )

    t2.set_upstream(t1)