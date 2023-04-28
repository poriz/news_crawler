from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.dummy import DummyOperator

import pendulum
from datetime import datetime, timedelta

from subpackages.links import makeLinks
from subpackages.contents import bringContents
from subpackages.final_processing import finalProcessing
from subpackages.StsProcessing import sts_module


local_tz = pendulum.timezone("Asia/Seoul")

link = makeLinks()
content = bringContents()
fin = finalProcessing()
sts = sts_module()

# 링크 생성
def mk_link(ex_time):
    link.make_links_func(ex_time)

# 크롤링 수행
def mk_contents(ex_time):
    content.make_contents(ex_time)

# 중복제거 및 병합
def mk_fin(ex_time):
    fin.fin_func(ex_time)

# DAG브런치 생성
def branch_func():
    import json
    with open('news2/subpackages/execution_time.json',"r") as t_data:
        json_data = json.load(t_data)

    # AM인 경우 drop수행
    if json_data["data"] =="AM":
        return 'fin_task'
    else:
        return 'stop_task'

def sts_tasks(ex_time):
    sts.sts_func(ex_time)


# ----------------------DAG 시작----------------------
default_args = {
    "owner" : "airflow",
    "start_date" : datetime(),
    "max_active_runs": 1,
    "retries": 0 , 
    "provide_context" : True,
}

dag_id = 'link_dag_ver2'

with DAG(
    dag_id =dag_id,
    user_defined_macros = {
        'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d"),
        'local_ampm' : lambda execution_date: execution_date.in_timezone(local_tz).strftime("%p")
    },
    default_args=default_args,
    schedule_interval="@once"
)as dag:

    make_link = PythonOperator(
        task_id = 'make_links',
        python_callable = mk_link,
        op_args={"{{ local_dt(execution_date) }}"}
    )

    bring_contents = PythonOperator(
        task_id = 'news_contents',
        python_callable = mk_contents,
        op_args={"{{local_ampm(execution_date)}}"}
    )

    branch_op = BranchPythonOperator(
        task_id = 'branch_task',
        python_callable = branch_func,
    )

    final_op = PythonOperator(
            task_id = "fin_task",
            python_callable = mk_fin,
            op_args = {"{{ local_dt(execution_date) }}"},

    )
    stop_op = DummyOperator(
        task_id='stop_task',
    )

    sts_op = PythonOperator(
        task_id = 'STS_task',
        python_callable = sts_tasks,
        op_args = {"{{ local_dt(execution_date) }}"},
    )

    # 다운 스트림 설정
    make_link >>bring_contents >> branch_op >> final_op >> sts_op
    make_link >>bring_contents >> branch_op >> stop_op
    