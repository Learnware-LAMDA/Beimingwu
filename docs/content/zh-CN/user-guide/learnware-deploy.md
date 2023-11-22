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
learnware = client.load_learnware(
    learnware_id=learnware_id, runnable_option="docker"
)
```

其中 `runnable_option` 有三种选项（默认为 `None`），分别对应下述三种加载学件环境的模式：

- `None`：仅加载学件规约与基本信息，使用当前运行 `learnware` 包的 `Python` 环境运行学件；
- `"conda"`：为每个学件安装独立的 `conda` 虚拟环境（运行结束后自动删除），在虚拟环境内独立运行每个学件；
- `"docker"`：在 `docker` 容器内安装 `conda` 虚拟环境（运行结束后自动销毁），在容器内独立运行每个学件（用户需要有 `docker` 权限）。

当用户需要根据 `id` 批量载入学件时，可以通过如下代码实现：
```python
learnware_ids = ["00000082","00000120"]
learnware_list = client.load_learnware(
    learnware_id=learnware_ids, runnable_option="docker"
)
```

需要注意的是，尽管系统已尽最大努力确保每个学件的安全，但如果仍有包含恶意代码的漏网之鱼，则 `None` 和 `"conda"` 两种模式是**不安全**的。如果用户不能确保需要加载的学件的安全性，请使用 `"docker"` 模式载入学件。


### 根据学件 `zip` 文件载入学件

除了根据学件 `id` 载入学件，用户还可以使用从网页端下载的 `zip` 文件载入学件：

```python
learnware_path = "learnware1.zip"
learnware_list = client.load_learnware(
    learnware_path=learnware_path, runnable_option="docker"
)
```

当用户需要批量载入 `zip` 格式的学件时，可以通过如下代码实现：
```python
learnware_paths = ["learnware1.zip", "learnware2.zip"]
learnware_list = client.load_learnware(
    learnware_path=learnware_paths, runnable_option="docker"
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

更详细的使用方法和原理介绍请参考：[Learnware 包复用方法介绍](#)。

### 使用有标记数据复用学件

当用户有少量有标记数据时，我们提供了`EnsemblePruning`和`FeatureAugmentReuser`两种方法帮助用户复用学件。

-  `EnsemblePruning` 通过选择性集成的方法选择更适合用户任务的学件：

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

更详细的使用方法和原理介绍请参考：[Learnware 包复用方法介绍](#)。

- `FeatureAugmentReuser`通过特征增广的方式帮助用户复用学件，原始学件的输出会拼接到用户任务的特征上，并基于有标记数据训练一个简单的模型（分类任务为logistics regression，回归任务为ridge）：

```python
from learnware.reuse import FeatureAugmentReuser

# mode="regression": 适用于回归任务
# mode="classification"：适用于分类任务
augment_reuser = FeatureAugmentReuser(
    learnware_list=learnware_list, mode="regression"
)

# (val_X, val_y) 为少量有标记数据
augment_reuser.fit(val_X, val_y)
predict_y = augment_reuser.predict(user_data=test_x) 
```

## 异构学件复用方法

我们提供了 `HeteroMapAlignLearnware` 类帮助用户将异构学件与用户任务进行对齐，一共包含两步：输入空间对齐、输出空间对齐。

在异构学件的对齐过程中，学件的统计规约和用户任务的统计规约 `user_spec` 将用于输入空间的对齐，少量有标记数据 `(val_x, val_y)` 将用于输出空间的对齐，具体代码如下：
```python
from learnware.reuse import HeteroMapAlignLearnware

# mode="regression": 用户任务类型为回归
# mode="classification"：用户任务类型为分类
hetero_learnware = HeteroMapAlignLearnware(learnware=leanrware, mode="regression")
hetero_learnware.align(user_spec, val_x, val_y)

# 使用对齐后的异构学件进行预测
predict_y = hetero_learnware.predict(user_data=test_x)
```

如果想要复用多个异构学件，可以将 `HeteroMapAlignLearnware` 和上文介绍的同构复用方法 `Averaging`、`EnsemblePruning` 相结合：

```python
hetero_learnware_list = []
for learnware in learnware_list:
    hetero_learnware = HeteroMapAlignLearnware(learnware, mode="regression")
    hetero_learnware.align(user_spec, val_x, val_y)
    hetero_learnware_list.append(hetero_learnware)
            
# 使用 AveragingReuser 复用多个异构学件
reuse_ensemble = AveragingReuser(learnware_list=hetero_learnware_list, mode="mean")
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)

# 使用 EnsemblePruningReuser 复用多个异构学件
reuse_ensemble = EnsemblePruningReuser(
    learnware_list=hetero_learnware_list, mode="regression"
)
reuse_ensemble.fit(val_x, val_y)
ensemble_pruning_predict_y = reuse_ensemble.predict(user_data=test_x)
```

