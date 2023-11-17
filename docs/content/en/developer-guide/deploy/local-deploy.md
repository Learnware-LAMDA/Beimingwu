# Deploying Beimingwu on a Single Machine

## Install Docker Compose
Visit the [Docker official website](https://docs.docker.com/compose/install/#installing-compose) and follow the official documentation to install `Docker Compose`.

## Deploy Using Docker Compose

Download the [backend code](https://github.com/Learnware-LAMDA/Beiming-System.git) and navigate to the `deploy/docker_compose` directory, then execute:

```shell
docker-compose -p learnware up -d
```

To uninstall, you can execute:

```shell
docker-compose -p learnware down
```