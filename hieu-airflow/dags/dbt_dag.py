"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig

# adjust for other database types
from cosmos.profiles import PostgresUserPasswordProfileMapping
from pendulum import datetime
import os

ENV = "dev"
YOUR_NAME = "hieuung"
CONNECTION_ID = "my_data_warehouse" if ENV == 'dev' else "my_data_warehouse"
DB_NAME = "postgres"
SCHEMA_NAME = "raw_layer"

# The path to the dbt project
DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/hieu_dbt_project"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

profile_config = ProfileConfig(
    profile_name="hieuung",
    target_name=ENV,
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=CONNECTION_ID,
        profile_args={"schema": SCHEMA_NAME},
    ),
)

dbt_args = {
        "install_deps": True,
    }

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)

default_args = {
        'owner' : 'hieuung',
    }

trigger_args = {
    "my_name": YOUR_NAME
    }

@dag(
    start_date=datetime(2023, 8, 1),
    schedule=None,
    catchup=False,
    default_args= default_args,
    params=trigger_args,
)
def my_simple_dbt_dag():
    start = EmptyOperator(task_id = 'start')

    transform_data = DbtTaskGroup(
        group_id="transform_data",
        project_config=ProjectConfig(DBT_PROJECT_PATH),
        profile_config=profile_config,
        execution_config=execution_config,
        operator_args={
            "vars": '{ \
                "my_name": {{ params.my_name }} \
                }',
            "install_deps": True
        },
        default_args={
            "retries": 0
            },
    )

    end = EmptyOperator(task_id = 'end')

    start >> transform_data >> end


my_simple_dbt_dag()