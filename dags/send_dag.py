# from dags.producer import MessageProducer
from datetime import datetime, timedelta
import pytz
from airflow import DAG
from airflow.operators.python import PythonOperator
import requests
import os
# from producer import MessageProducer
from producer import MessageProducer


KAFKA_BROKERS=os.getenv("KAFKA_BROKERS").split(',')
KAFKA_CONSUMER_GROUP="taehoon"


default_args = {
    "owner": "taehoon",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
tz = pytz.timezone("Asia/Seoul")


def send():
    brokers = KAFKA_BROKERS
    topic = "send-message-topic"
    producer = MessageProducer(brokers, topic)
    producer.send_message({'num': '30'})


with DAG(
    default_args=default_args,
    dag_id="taehoon_dag",
    description="send_post",
    start_date=datetime(2023, 9, 8, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
    max_active_runs=1
) as dag:
    task1 = PythonOperator(
        task_id="send", 
        python_callable=send,
    )
    
    task1
    
    
