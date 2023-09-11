from datetime import datetime, timedelta
import pytz
import os
import json

from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaProducer


default_args = {
    "owner": "donghyun",
    "retries": 5,
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
    ticker = "005930"
    producer.send("airflow-flask-crawling", {"ticker": ticker})
    producer.send("airflow-elk-crawling", {"ticker": ticker})
    producer.close()


with DAG(
    dag_id="send_crawling_op",
    default_args=default_args,
    start_date=datetime(2023, 9, 1, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = PythonOperator(task_id="task1", python_callable=send)

    task1
