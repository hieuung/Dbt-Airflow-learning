from airflow import DAG
from datetime import datetime
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


# Step 2: Initiating the default_args
default_args = {
        'owner' : 'hieuung',
    }

dag =  DAG(
    dag_id="populate_data_warehouse",
    default_args=default_args,
    start_date=datetime(2024, 4, 12),
    schedule_interval='@once',
    catchup=True,
    is_paused_upon_creation=True
)

start = EmptyOperator(task_id = 'start')

initialize = PostgresOperator(
    task_id="initialize",
    postgres_conn_id="my_data_warehouse",
    sql="sql/northwind.sql",
    dag=dag
)

end = EmptyOperator(task_id = 'end')

start >> initialize >> end