from datetime import datetime, timedelta
import pytz

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "donghyun",
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
}
tz = pytz.timezone("Asia/Seoul")

with DAG(
    dag_id="catchup_backfill",
    default_args=default_args,
    start_date=datetime(2023, 5, 19, tzinfo=tz),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    task1 = BashOperator(task_id="task1", bash_command="echo Hello World!")
