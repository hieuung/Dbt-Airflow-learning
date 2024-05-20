docker run \
  --name=test-dbt \
  --network=host \
  --mount type=bind,source=./dbt,target=/usr/app \
  --mount type=bind,source=./profiles.yml,target=/root/.dbt/profiles.yml \
  hieuung/test-dbt \
  build && sleep infinity