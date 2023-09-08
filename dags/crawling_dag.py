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


def test(ti):
    producer = KafkaProducer(
        bootstrap_servers=brokers,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        acks=0,
        api_version=(3, 4, 1),
        retries=3,
    )
    ticker = "005930"
    producer.send("airflow-crawling-msg", {"ticker": ticker})
    producer.send("elk-logs-airflow", {"ticker": ticker})
    producer.close()


with DAG(
    dag_id="send_crawling_op",
    default_args=default_args,
    start_date=datetime(2023, 9, 1, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task2 = PythonOperator(task_id="asd", python_callable=test)

    task2
