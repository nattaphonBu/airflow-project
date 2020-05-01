import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.docker_operator import DockerOperator

from utils import send_alert_task_failure_to_slack


LOG_DIRECTORY = os.environ.get('LOG_DIRECTORY')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
DYNAMODB_URL = os.environ.get('DYNAMODB_URL')
BOTO_CREDENTIAL = os.environ.get('BOTO_CREDENTIAL')
SCHEDULE_TIME = '*/30 * * * *'
IMAGE_NAME = os.environ.get('IMAGE_NAME')
ENVIRONMENT_SETTING = os.environ.get('ENVIRONMENT_SETTING')
COMMAND = 'python pronto_dashboard/manage.py update_keywords_difficulty --settings=pronto_dashboard.settings.' + ENVIRONMENT_SETTING

default_args = {
    'owner': 'ProntoTools',
    'description': 'update keywords difficulty run every 30 minute',
    'depend_on_past': False,
    'start_date': datetime(2020, 2, 18),
    'retries': 1,
    'retry_on_failure': timedelta(minutes=5),
    'on_failure_call_back': send_alert_task_failure_to_slack
}

with DAG('update_keywords_difficulty_pipeline', default_args=default_args, schedule_interval=SCHEDULE_TIME, catchup=False) as dag:

    t1=BashOperator(
        task_id='login_aws',
        bash_command='$(aws ecr get-login --region eu-west-1 --no-include-email)'
    )

    t2=DockerOperator(
        task_id='sent_ketwords_to_authoritylabs_pipeline',
        auto_remove=True,
        container_name='pronto-app',
        image=IMAGE_NAME,
        api_version='auto',
        command=COMMAND,
        docker_url='unix://var/run/docker.sock',
        network_mode='host',
        environment={
            'DATABASE_HOST': DATABASE_HOST,
            'ELASTICSEARCH_URL': ELASTICSEARCH_URL,
            'DYNAMODB_URL': DYNAMODB_URL,
        },
        volumes=[LOG_DIRECTORY, BOTO_CREDENTIAL],
        force_pull=True,
    )

    t2.set_upstream(t1)
