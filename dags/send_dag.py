from datetime import datetime, timedelta
import pytz
import os
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer


default_args = {
    "owner": "taehoon",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
tz = pytz.timezone("Asia/Seoul")
brokers = os.getenv("KAFKA_BROKERS").split(",")


def send(ti):
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        acks=0,
        api_version=(3, 4, 1),
        retries=3,
    )
    producer.send("airflow-flask-weather", {"num": "30"})
    producer.send("airflow-elk-weather", {"num": "30"})
    producer.close()


with DAG(
    default_args=default_args,
    dag_id="taehoon_dag",
    description="send_post",
    start_date=datetime(2023, 9, 8, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1,
) as dag:
    task1 = PythonOperator(
        task_id="send",
        python_callable=send,
    )

    task1
