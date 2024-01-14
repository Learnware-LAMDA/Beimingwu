# Deploying Beimingwu on a Single Machine

## Install Docker Compose
Visit the [Docker official website](https://docs.docker.com/compose/install/#installing-compose) and follow the official documentation to install `Docker Compose`.

## Deploy Using Docker Compose

Download the [backend code](https://gitee.com/beimingwu/beimingwu.git) and navigate to the `deploy/docker_compose` directory.

## Prepare Files
Prepare miniconda installation file
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.9.0-0-Linux-x86_64.sh -O miniconda_install.sh
```

Prepare source code
```shell
mkdir -p Beimingwu/deploy/
cp -r ../../backend Beimingwu/
cp -r ../../frontend Beimingwu/
cp -r ../static Beimingwu/deploy/
git clone https://gitee.com/beimingwu/learnware.git
```

## Build Image
```shell
sudo docker compose -f docker-compose.yaml build
```

## Run Docker Container
```shell
sudo docker compose -f docker-compose.yaml -p learnwaresingle up -d
```

## Check Container Status
```shell
$ sudo docker ps | grep learnware
f8faeefbcad7   lamda/bm-system-backend:0.0.1          "/opt/nvidia/nvidia_…"   6 seconds ago   Up 4 seconds   8088/tcp                                            learnware-monitor
560fc4ae3127   lamda/bm-system-backend:0.0.1          "/opt/nvidia/nvidia_…"   6 seconds ago   Up 4 seconds   8088/tcp                                            learnware-backend
7b1fd9b5b3fc   lamda/bm-system-admin-frontend:0.0.1   "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds   80/tcp, 0.0.0.0:5174->5173/tcp, :::5174->5173/tcp   learnware-admin-frontend
7065cd6c0944   lamda/bm-system-frontend:0.0.1         "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds   80/tcp, 0.0.0.0:5173->5173/tcp, :::5173->5173/tcp   learnware-frontend
fce2f3102e62   redis                                  "docker-entrypoint.s…"   6 seconds ago   Up 4 seconds   6379/tcp                                            learnware-redis
```

## Visite the Website
admin frontend: http://127.0.0.1:5174

frontend: http://127.0.0.1:5173

default admin account:
- username: admin@localhost 
- password: admin

## Stop Container
```shell
sudo docker compose -f docker-compose.yaml -p learnwaresingle down
```