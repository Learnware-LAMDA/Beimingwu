# Deploying Beimingwu System on Kubernetes

## Deploy Dependencies
### Deploy Default Storage Class
Beimingwu System will use the cluster's default storage class to create the required storage. You can refer to the concept of [Kubernetes Default Storage Class](https://kubernetes.io/docs/tasks/administer-cluster/change-default-storage-class/) for more information. For example, if you are using rook-cephfs as your default storage class, you can execute the following command to set it:

```shell
kubectl patch storageclass rook-cephfs -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

### Deploy Postgres Database
Clone the [PostgresOperator](https://github.com/zalando/postgres-operator.git) repository and follow the installation instructions from the repository. Here's an example:

#### Deploy PostgresOperator
```shell
# First, clone the repository and change to the directory
git clone https://github.com/zalando/postgres-operator.git
cd postgres-operator

# Apply the manifests in the following order
kubectl create -f manifests/configmap.yaml  # configuration
kubectl create -f manifests/operator-service-account-rbac.yaml # identity
kubectl create -f manifests/postgres-operator.yaml  # deployment
kubectl create -f manifests/api-service.yaml  # operator API to be used by UI
```

#### Deploy Postgres Instance
```shell
kubectl create -f manifests/minimal-postgres-manifest.yaml
```

### Deploy Redis
Clone the [RedisOperator](https://github.com/spotahome/redis-operator.git) repository and follow the installation instructions from the repository. Here's an example:

#### Deploy RedisOperator
```shell
REDIS_OPERATOR_VERSION=v1.3.0
kubectl create -f https://raw.githubusercontent.com/spotahome/redis-operator/${REDIS_OPERATOR_VERSION}/manifests/databases.spotahome.com_redisfailovers.yaml
kubectl apply -f https://raw.githubusercontent.com/spotahome/redis-operator/${REDIS_OPERATOR_VERSION}/example/operator/all-redis-operator-resources.yaml
```

#### Deploy Redis Instance
```shell
REDIS_OPERATOR_VERSION=v1.2.4
kubectl create -f https://raw.githubusercontent.com/spotahome/redis-operator/${REDIS_OPERATOR_VERSION}/example/redisfailover/basic.yaml
```

## Deploy Backend
### Download Deployment Files
```shell
git clone https://github.com/Learnware-LAMDA/Beiming-System.git
cd Beiming-System/deploy/kubernetes
```

### Configure Files
Set the configuration files for the backend `config.json`:

```json
{
    "database": {
        "type": "sqlalchemy",
        // Set the database address
        "url": "postgresql+psycopg2://username:password@postgres-server.default/learnware_backend"
    },
    // Backend host, no need to change
    "backend_host": "learnware-backend-cluster.learnware",
    // Verify learnware timeout
    "verify_timeout": 3600,
    // Set the proxy used for learnware verification, can be empty
    "verify_proxy": "",

    "email": {
        // Email for sending verification emails
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

Set the configuration file for learnware packages `config_learnware.json`:

```json
{
    // Do not set the database name
    "database_url": "postgresql+psycopg2://username:password@postgres-server.default"
}
```

Execute the following commands:

```shell
kubectl create ns learnware
kubectl create configmap learnware-backend -n learnware --from-file=config.json
kubectl create configmap learnware -n learnware --from-file=config_learnware.json

IMAGE_NAME="lamda/bm-system-backend:0.0.1"
cat backend.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | kubectl apply -f -
```

## Deploy Frontend
Navigate to the deploy directory and execute:

```shell
IMAGE_NAME="lamda/bm-system-frontend:0.0.1"
cat frontend.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | kubectl apply -f -
```

## Deploy Admin Frontend
Navigate to the deploy directory and execute:

```shell
IMAGE_NAME="lamda/bm-system-admin-frontend:0.0.1"
cat admin-frontend.yaml \
  | sed "s#{{IMAGE_NAME}}#$IMAGE_NAME#g" \
  | kubectl apply -f -
```

## Check Pod Status
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

## Uninstall
```shell
kubectl delete ns learnware
```