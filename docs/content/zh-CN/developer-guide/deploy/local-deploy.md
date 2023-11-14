# 在单机上部署北冥坞系统

## 安装 Docker Compose
到 [Docker官网](https://docs.docker.com/compose/install/#installing-compose)，根据官方文档的指引安装 `docker compose`。

## 使用 Docker Compose 部署

下载 [后端代码](https://github.com/Learnware-LAMDA/Beiming-System.git)，进入 `deploy/docker_compose` 目录，执行：
```shell
docker-compose -p learnware up -d
```
若要卸载，可执行：
```shell
docker-compose -p learnware down
```