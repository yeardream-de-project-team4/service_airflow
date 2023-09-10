from datetime import datetime, timedelta
import pytz
import json

from airflow import DAG
from airflow.providers.apache.kafka.operators.produce import (
    ProduceToTopicOperator,
)


default_args = {
    "owner": "eom",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
tz = pytz.timezone("Asia/Seoul")


def send_message():
    return {"k": json.dumps({"num": "20"})}.items()


def send_log():
    return {"k": json.dumps({"num": "20"})}.items()


with DAG(
    default_args=default_args,
    dag_id="upbit_trade",
    description="send_post",
    start_date=datetime(2023, 9, 8, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
) as dag:
    task1 = ProduceToTopicOperator(
        kafka_config_id="aws_kafka",
        task_id="airflow-flask-market",
        topic="airflow-flask-market",
        producer_function=send_message,
    )

    task2 = ProduceToTopicOperator(
        kafka_config_id="aws_kafka",
        task_id="airflow-elk-market",
        topic="airflow-elk-market",
        producer_function=send_log,
    )

    task1 >> task2
