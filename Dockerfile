# ARG py_version=3.11.2

# FROM python:$py_version-slim-bullseye as base

# RUN apt-get update \
#   && apt-get dist-upgrade -y \
#   && apt-get install -y --no-install-recommends \
#     build-essential=12.9 \
#     ca-certificates=20210119 \
#     git=1:2.30.2-1+deb11u2 \
#     libpq-dev=13.14-0+deb11u1 \
#     make=4.3-4.1 \
#     openssh-client=1:8.4p1-5+deb11u3 \
#     software-properties-common=0.96.20.2-2.1 \
#   && apt-get clean \
#   && rm -rf \
#     /var/lib/apt/lists/* \
#     /tmp/* \
#     /var/tmp/*

# ENV PYTHONIOENCODING=utf-8
# ENV LANG=C.UTF-8

# RUN python -m pip install --upgrade "pip==24.0" "setuptools==69.2.0" "wheel==0.43.0" --no-cache-dir


# FROM base as dbt-core

# ARG commit_ref=main

# HEALTHCHECK CMD dbt --version || exit 1

# WORKDIR /usr/app/dbt/
# ENTRYPOINT ["dbt"]

# RUN python -m pip install --no-cache-dir "dbt-core @ git+https://github.com/dbt-labs/dbt-core@${commit_ref}#subdirectory=core"

# FROM base as dbt-postgres

# ARG commit_ref=main

# HEALTHCHECK CMD dbt --version || exit 1

# WORKDIR /usr/app/dbt/
# ENTRYPOINT ["dbt"]

# RUN python -m pip install --no-cache-dir "dbt-postgres @ git+https://github.com/dbt-labs/dbt-core@${commit_ref}#subdirectory=plugins/postgres"

# FROM dbt-core as dbt-third-party

# ARG dbt_third_party

# RUN if [ "$dbt_third_party" ]; then \
#         python -m pip install --no-cache-dir "${dbt_third_party}"; \
#     else \
#         echo "No third party adapter provided"; \
#     fi \

FROM apache/airflow:2.7.1
RUN pip install --upgrade pip && \
    pip install astronomer-cosmos==1.0.4 && \
    pip install elementary-data

USER root
RUN apt-get update -y && \
    apt-get install pkg-config -y && \
    apt-get install libpq-dev -y && \
    apt-get install python3-dev default-libmysqlclient-dev build-essential -y
USER 1001

# replace dbt-postgres with another supported adapter if you're using a different warehouse type
RUN python -m venv dbt_venv && source dbt_venv/bin/activate

ENV PIP_USER=false

COPY requirements.txt requirements.txt
RUN ${AIRFLOW_HOME}/dbt_venv/bin/pip install --upgrade pip && \
    ${AIRFLOW_HOME}/dbt_venv/bin/pip install -r requirements.txt --no-cache-dir

