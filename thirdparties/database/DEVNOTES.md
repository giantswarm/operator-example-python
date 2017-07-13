

https://hub.docker.com/_/postgres/

VOLUME /var/lib/postgresql/data
https://github.com/docker-library/postgres/blob/dd88d2f02ad0f9852a7b33a8b542e14f5867b0c1/9.6/alpine/docker-entrypoint.sh

```yaml
kind: database
[..]
  type: postgres
  # version: min/max
  database:
    name: (from configmap? nö)
    user:
    password: (secret-name?)

    locales:
    type:
    init: (from volume)

    # backup: or extra kind..
```
$POSTGRES_DB

https://github.com/docker-library/postgres/blob/dd88d2f02ad0f9852a7b33a8b542e14f5867b0c1/9.6/alpine/docker-entrypoint.sh#L4

file_env 'POSTGRES_INITDB_ARGS'
file_env 'POSTGRES_PASSWORD'
file_env 'POSTGRES_USER' 'postgres'
file_env 'POSTGRES_DB' "$POSTGRES_USER"

root user? "postgres"?
`superuser`



https://github.com/kubernetes/charts/tree/master/stable/postgresql
https://github.com/kubernetes/charts/tree/master/stable/postgresql#metrics


run this in a container, connecting to database-server as root
read data from `secret`? or mixture of `configmap`/`secret`


```bash
# FIXME also set password

#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER docker;
      CREATE USER tom WITH PASSWORD 'myPassword';
    CREATE DATABASE docker;
    GRANT ALL PRIVILEGES ON DATABASE docker TO docker;
EOSQL
```


---

https://github.com/kubernetes/charts/tree/master/incubator/patroni#connecting-to-postgres
https://github.com/kubernetes/charts/tree/master/incubator/patroni#configuration
