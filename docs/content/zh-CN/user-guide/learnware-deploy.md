# 如何部署和复用学件？

在北冥系统中，用户可以使用 `learnware` Python 包对学件进行部署和复用。

## 学件和环境的载入

用户可以使用 `learnware` Python 包中的 `LearnwareClient` 载入学件，首先定义 `LearnwareClient`:

```python
from learnware.client import LearnwareClient
client = LearnwareClient()
```

### 根据学件 `id` 载入学件
假设用户已知需要载入的学件对应的 `id`，那么可以使用如下代码载入对应的学件和环境：

```python
learnware_id = "00000082"
learnware_list = client.load_learnware(
    learnware_id=learnware_id, runnable_option="docker"
)
```

其中 `runnable_option` 有四种选项，分别对应下述四种加载学件环境的模式：
- `None`：仅加载学件规约与基本信息，学件此时无法运行；
- `"normal"`：不另外安装环境，直接使用当前运行 `learnware` 包的 `Python` 环境运行学件；
- `"conda_env"`：为每个学件安装独立的 `conda` 虚拟环境（运行结束后自动删除），在虚拟环境内独立运行每个学件；
- `"docker"`：在 `docker` 容器内安装 `conda` 虚拟环境（运行结束后自动销毁），在容器内独立运行每个学件（用户需要有 `docker` 权限）。

需要注意的是，尽管系统已尽最大努力确保每个学件的安全，但如果仍有包含恶意代码的漏网之鱼，则 `"normal"` 和 `"conda_env"` 两种模式是**不安全**的。如果用户不能确保需要加载的学件的安全性，请使用 `"docker"` 模式载入学件。


### 根据学件 `zip` 文件载入学件

除了根据学件 `id` 载入学件，用户还可以使用从网页端下载的 `zip` 文件载入学件：

```python
learnware_path = "learnware1.zip"
learnware_list = client.load_learnware(
    learnware_path=learnware_path, runnable_option="docker"
)
```

## 同构学件复用方法

除了直接运行学件，用户还可以基于系统提供的学件复用方法，进一步对无标记数据进行预测。

复用方法主要分为两类：（1）直接复用；（2）基于用户的少量有标记数据复用。

### 直接复用学件

我们提供了 `JobSelector` 和 `Averaging` 两种直接复用学件的方法:

- `JobSelector` 通过训练分类器为不同的数据选择不同的学件进行预测，具体代码如下：
```python
from learnware.reuse import JobSelectorReuser

# learnware_list 是已载入的学件 list
reuse_job_selector = JobSelectorReuser(learnware_list=learnware_list)

# test_x 是用户任务的待预测数据，predict_y 是复用学件的预测结果
predict_y = reuse_job_selector.predict(user_data=test_x)
```
- `Averaging` 使用平均集成的方法进行学件复用，其中 `mode` 表示具体的集成方式：
```python
from learnware.reuse import AveragingReuser

# mode="mean": 适用于回归任务，对学件输出进行平均
# mode="vote_by_label"：适用于分类任务，对学件输出的标签采用大多数投票的方式集成
# mode="vote_by_prob"：适用于分类任务，对学件输出的标签概率采用大多数投票的方式集成
reuse_ensemble = AveragingReuser(
    learnware_list=learnware_list, mode="vote_by_label"
)
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)
```

更详细的使用方法和原理介绍请参考：[Learnware 包复用方法介绍](link)。

### 使用有标记数据复用学件

当有少量的有标记数据时，可以通过 `EnsemblePruning` 方法复用学件。该方法基于少量有标记数据，通过选择性集成的方法选择更适合用户任务的学件：

```python
from learnware.reuse import EnsemblePruningReuser

# mode="regression": 适用于回归任务
# mode="classification"：适用于分类任务
reuse_ensemble_pruning = EnsemblePruningReuser(
    learnware_list=learnware_list, mode="regression"
)

# (val_X, val_y) 为少量有标记数据
reuse_ensemble_pruning.fit(val_X=val_X, val_y=val_y)
predict_y = reuse_job_selector.predict(user_data=test_x) 
```

更详细的使用方法和原理介绍请参考：[Learnware 包复用方法介绍](link)。


## 异构学件复用方法
