# Deploying Beimingwu on a Single Machine

## Install Docker Compose
Visit the [Docker official website](https://docs.docker.com/compose/install/#installing-compose) and follow the official documentation to install `Docker Compose`.

## Deploy Using Docker Compose

Download the [backend code](https://github.com/Learnware-LAMDA/Beiming-System.git) and navigate to the `deploy/docker_compose` directory.

### prepare files
prepare miniconda installation file
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.9.0-0-Linux-x86_64.sh -O miniconda_install.sh
```

prepare source code
```shell
mkdir -p Beiming-System/deploy/
cp -r ../../backend Beiming-System/
cp -r ../../frontend Beiming-System/
cp -r ../static Beiming-System/deploy/
git clone https://github.com/Learnware-LAMDA/Learnware.git
```

### build image
```shell
sudo docker compose -f docker-compose.yaml build
```

### run docker container
```shell
sudo docker compose -f docker-compose.yaml -p learnwaresingle up -d
```

### check container status
```shell
$ sudo docker ps | grep learnware
f8faeefbcad7   lamda/bm-system-backend:0.0.1          "/opt/nvidia/nvidia_…"   6 seconds ago   Up 4 seconds   8088/tcp                                            learnware-monitor
560fc4ae3127   lamda/bm-system-backend:0.0.1          "/opt/nvidia/nvidia_…"   6 seconds ago   Up 4 seconds   8088/tcp                                            learnware-backend
7b1fd9b5b3fc   lamda/bm-system-admin-frontend:0.0.1   "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds   80/tcp, 0.0.0.0:5174->5173/tcp, :::5174->5173/tcp   learnware-admin-frontend
7065cd6c0944   lamda/bm-system-frontend:0.0.1         "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds   80/tcp, 0.0.0.0:5173->5173/tcp, :::5173->5173/tcp   learnware-frontend
fce2f3102e62   redis                                  "docker-entrypoint.s…"   6 seconds ago   Up 4 seconds   6379/tcp                                            learnware-redis
```

### visite the website
admin frontend: http://127.0.0.1:5174

frontend: http://127.0.0.1:5173

default admin account:
- username: admin@localhost 
- password: admin

### stop container
```shell
sudo docker compose -f docker-compose.yaml -p learnwaresingle down
```