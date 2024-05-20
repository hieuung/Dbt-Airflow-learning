"""
### Run a dbt Core project as a task group with Cosmos

Simple DAG showing how to run a dbt project as a task group, using
an Airflow connection and injecting a variable into the dbt project.
"""

from airflow.decorators import dag
from airflow.operators.empty import EmptyOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, DbtDag

# adjust for other database types
from pendulum import datetime
import os

# The path to the dbt project
DBT_PROJECT_PATH = f"{os.environ['AIRFLOW_HOME']}/dags/dbt/hieu_dbt_project"
# The path where Cosmos will find the dbt executable
# in the virtual environment created in the Dockerfile
DBT_EXECUTABLE_PATH = f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"

elementary_profile_config = ProfileConfig(
    profile_name="elementary",
    target_name='default',
    profiles_yml_filepath=f"{os.environ['AIRFLOW_HOME']}/dags/dbt/profiles.yml"
)

execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE_PATH,
)

elementary = DbtDag(
    project_config=ProjectConfig(DBT_PROJECT_PATH),
    profile_config=elementary_profile_config,
    execution_config=execution_config,
    operator_args={
        "install_deps": True,  # install any necessary dependencies before running any dbt command
    },
    # normal dag parameters
    schedule_interval=None,
    start_date=datetime(2024, 4, 12),
    catchup=False,
    dag_id="elementary",
    default_args={"retries": 0},
)

elementary