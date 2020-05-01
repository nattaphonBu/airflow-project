from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.hooks.base_hook import BaseHook


SLACK_CONNECTION_ID = 'slack'

def send_alert_task_failure_to_slack(context):
    slack_webhook_token = BaseHook.get_connection(SLACK_CONNECTION_ID).password
    slack_msg = """
        :red_circle: Task Failed. 
        *Task*: {task}  
        *Dag*: {dag} 
        *Execution Time*: {exec_date}
        *Task Instant*: {task_instant}
        *Log Url*: {log_url} 
        """.format(
            task=context.get('task_instance').task_id,
            dag=context.get('task_instance').dag_id,
            task_instant=context.get('task_instance'),
            exec_date=context.get('execution_date'),
            log_url=context.get('task_instance').log_url,
        )
    failed_alert = SlackWebhookOperator(
        task_id='slack_test',
        http_conn_id='slack',
        webhook_token=slack_webhook_token,
        message=slack_msg,
        username='airflow'
    )
    return failed_alert.execute(context=context)