# 在kubernetes上部署北冥系统

## 部署依赖组件
### 部署默认存储类
北冥系统会使用集群默认的存储类来创建所需要的存储。关于kubernetes默认存储类的概念可以参考[Kubernetes默认存储类](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/)。比如，如果您使用rook-cephfs作为您的默认存储类，可以执行以下命令来设置：
```shell
kubectl patch storageclass rook-cephfs -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

### 部署Postgres数据
克隆[PostgresOperator](https://github.com/zalando/postgres-operator.git)仓库。并按照仓库说明进行安装，以下为举例。
#### 部署PostgresOperator
```shell
# First, clone the repository and change to the directory
git clone https://github.com/zalando/postgres-operator.git
cd postgres-operator

# apply the manifests in the following order
kubectl create -f manifests/configmap.yaml  # configuration
kubectl create -f manifests/operator-service-account-rbac.yaml  # identity and permissions
kubectl create -f manifests/postgres-operator.yaml  # deployment
kubectl create -f manifests/api-service.yaml  # operator API to be used by UI
```
#### 部署Postgres实例
```shell
kubectl create -f manifests/minimal-postgres-manifest.yaml
```

### 部署Redis
克隆[RedisOperator](https://github.com/spotahome/redis-operator.git)仓库，并按照仓库说明进行安装，以下为举例：
#### 部署RedisOperator
```shell
REDIS_OPERATOR_VERSION=v1.3.0
kubectl create -f https://raw.githubusercontent.com/spotahome/redis-operator/${REDIS_OPERATOR_VERSION}/manifests/databases.spotahome.com_redisfailovers.yaml
kubectl apply -f https://raw.githubusercontent.com/spotahome/redis-operator/${REDIS_OPERATOR_VERSION}/example/operator/all-redis-operator-resources.yaml
```
#### 部署Redis实例
```shell
REDIS_OPERATOR_VERSION=v1.2.4
kubectl create -f https://raw.githubusercontent.com/spotahome/redis-operator/${REDIS_OPERATOR_VERSION}/example/redisfailover/basic.yaml
```

## 部署后端
### 下载部署文件
```shell
git clone https://github.com/Learnware-LAMDA/Beiming-System.git
cd Beiming-System/deploy/kubernetes
```
### 设置配置文件
设置后端的配置文件config.json:
```json
{
    "database": {
        "type": "sqlalchemy",
        // 数据库地址设置
        "url": "postgresql+psycopg2://username:password@postgres-server.default/learnware_backend"
    },
    // 后端地址设置，无需改动
    "backend_host": "learnware-backend-cluster.learnware",
    // 验证学件超时时间
    "verify_timeout": 3600,
    // 设置验证学件时使用的代理，可为空
    "verify_proxy": "",

    "email": {
        // 发送验证邮件的邮箱
        "smtp_server": "",
        "smtp_port": 465,
        "smtp_ssl": true,
        "smtp_username": "",
        "smtp_password": "",
        "sender_email": "",
        "verification_url": "https://www.lamda.nju.edu.cn/learnware/#verify_email",
        "reset_password_url": "https://www.lamda.nju.edu.cn/learnware/#reset_password",
        "proxy_host": "",
        "proxy_port": -1
    }
}
```
设置学件包的配置文件config_learnware.json
```json
{
    // 不要设置数据库名
    "database_url": "postgresql+psycopg2://username:password@postgres-server.default"
}
```
执行命令：
```shell
kubectl create ns learnware
kubectl create configmap learnware-backend -n learnware --from-file=config.json
kubectl create configmap learnware -n learnware --from-file=config_learnware.json

IMAGE_NAME="lamda/bm-system-backend:0.0.1"
cat deployment.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | kubectl apply -f -
```

## 部署前端
进入deploy目录执行
```shell
IMAGE_NAME="lamda/bm-system-frontend:0.0.1"
cat deployment.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | kubectl apply -f -
```

## 部署管理前端
进入deploy目录执行
```shell
IMAGE_NAME="lamda/bm-system-admin-frontend:0.0.1"
cat deployment.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | kubectl apply -f -
```

## 检查pod运行情况
```shell
$ kubectl get pods -n learnware
NAME                                        READY   STATUS      RESTARTS       AGE
backup-data-28320660-rblp2                  0/1     Completed   0              12h
learnware-admin-frontend-64fdbf8df7-6tsff   1/1     Running     0              3h18m
learnware-backend-0                         1/1     Running     0              94m
learnware-docs-fb8495555-6l54p              1/1     Running     6 (7d7h ago)   19d
learnware-frontend-6479f7bcb5-t5sx5         1/1     Running     0              3h18m
learnware-system-docs-79df779cb4-f9tgz      1/1     Running     0              4d13h
monitor-learnware-verify-0                  1/1     Running     0              94m
```
