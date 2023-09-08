from datetime import datetime, timedelta
import pytz
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
import json

KAFKA_BROKERS = os.getenv("KAFKA_BROKERS").split(",")

default_args = {
    "owner": "eom",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}
tz = pytz.timezone("Asia/Seoul")

def send_message():
    return {'key': json.dumps({'sple': 'data'})}.items()


with DAG(
    dag_id="upbit_trade",
    default_args=default_args,
    start_date=datetime(2023, 9, 1, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    # t0 = PythonOperator(
    #     task_id="load_connections",
    #     python_callable=load_connections)

    task1 = ProduceToTopicOperator(
        kafka_config_id="aaa",
        task_id="produce_to_topic",
        topic="eom-flask-topic",
        producer_function=send_message
)
