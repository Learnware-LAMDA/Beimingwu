# 在单机上部署北冥系统

## 安装Docker Compose
到[Docker官网](https://docs.docker.com/compose/install/#installing-compose)，根据官方文档的指引安装docker compose

## 下载部署文件
下载后端代码(https://github.com/Learnware-LAMDA/Beiming-System.git),进入deploy/docker_compose目录

## 使用Docker Compose安装
执行
```shell
docker-compose -p learnware up -d
```

## 卸载
执行
```shell
docker-compose -p learnware down
```