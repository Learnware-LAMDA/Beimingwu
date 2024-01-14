# 在单机上部署北冥坞系统

## 安装 Docker Compose
到 [Docker官网](https://docs.docker.com/compose/install/#installing-compose)，根据官方文档的指引安装 `docker compose`。

## 使用 Docker Compose 部署

下载 [后端代码](https://gitee.com/beimingwu/beimingwu.git)，进入 `deploy/docker_compose` 目录。

### 准备文件
miniconda 安装文件
```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.9.0-0-Linux-x86_64.sh -O miniconda_install.sh
```
源代码文件
```shell
mkdir -p Beimingwu/deploy/
cp -r ../../backend Beimingwu/
cp -r ../../frontend Beimingwu/
cp -r ../static Beimingwu/deploy/
git clone https://gitee.com/beimingwu/learnware.git
```

### 构建镜像
```shell
sudo docker compose -f docker-compose.yaml build
```

### 启动容器
```shell
sudo docker compose -f docker-compose.yaml -p learnwaresingle up -d
```

### 检查容器状态
```shell
$ sudo docker ps | grep learnware
f8faeefbcad7   lamda/bm-system-backend:0.0.1          "/opt/nvidia/nvidia_…"   6 seconds ago   Up 4 seconds   8088/tcp                                            learnware-monitor
560fc4ae3127   lamda/bm-system-backend:0.0.1          "/opt/nvidia/nvidia_…"   6 seconds ago   Up 4 seconds   8088/tcp                                            learnware-backend
7b1fd9b5b3fc   lamda/bm-system-admin-frontend:0.0.1   "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds   80/tcp, 0.0.0.0:5174->5173/tcp, :::5174->5173/tcp   learnware-admin-frontend
7065cd6c0944   lamda/bm-system-frontend:0.0.1         "/docker-entrypoint.…"   6 seconds ago   Up 4 seconds   80/tcp, 0.0.0.0:5173->5173/tcp, :::5173->5173/tcp   learnware-frontend
fce2f3102e62   redis                                  "docker-entrypoint.s…"   6 seconds ago   Up 4 seconds   6379/tcp                                            learnware-redis
```

### 访问网站
管理页面: http://127.0.0.1:5174

前端页面: http://127.0.0.1:5173

默认管理员账户:
- 用户名: admin@localhost 
- 密码: admin

### 卸载
```shell
sudo docker compose -f docker-compose.yaml -p learnwaresingle down
```