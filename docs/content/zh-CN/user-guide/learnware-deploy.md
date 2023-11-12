# 如何部署和复用学件？

在北冥系统中，用户可以使用 `learnware` Python 包对学件进行部署和复用。

## 学件和环境的载入

用户可以使用`learnware` Python 包中的 `LearnwareClient` 载入学件，首先定义 `LearnwareClient`:

```python
from learnware.client import LearnwareClient
client = LearnwareClient()
```

### 根据学件 `id` 载入学件
假设用户已知需要载入的学件对应的 `id`，那么可以使用如下代码载入对应的学件和环境：

```python
learnware_id = ["00000084", "00000154", "00000155"] # 假设已知学件 id
learnware_list = client.load_learnware(learnware_id=learnware_id, runnable_option="docker")
```

其中 `runnable_option` 有三种选项，分别对应三种装载学件环境的模式
- 如果 `runnable_option` 等于 `"normal"` 或者 `None`，那么将使用当前运行 `learnware` 包的 `Python` 环境直接运行学件，不进行学件环境的装载。

- 如果 `runnable_option` 等于 `"conda"`，那么将为每个学件新建独立的 `conda` 虚拟环境装载对应的环境依赖，并独立运行每个学件。

- 如果 `runnable_option` 等于 `"docker"`，那么在 `docker` 内使用 `conda` 装载和独立运行每个学件。

主要注意的是，如果学件中包含恶意代码，`"normal"` 和 `"conda"` 两种模式是**不安全**的。如果用户不能确保需要装载学件的安全性，那么**务必**使用`"docker"`模式进行学件的载入。


### 根据学件 `zip` 文件载入学件

除了根据学件 `id` 载入学件，用户还可以使用从网页端下载的`zip` 文件载入学件和对应的环境。代码如下：

```python
learnware_path = ["learnware1.zip", "learnware2.zip", "learnware3.zip"] # 假设已知学件下载后的 zip 文件本地路径
learnware_list = client.load_learnware(learnware_path=learnware_id, runnable_option="docker")
```

## 同构学件复用方法

我们可以复用载入的学件并对用户的无标记数据进行预测。除了直接复用学件进行预测外，也可以利用用户任务的有标记数据来复用学件。

### 直接复用学件

我们提供了 `JobSelector` 和 `Averaging` 两种直接复用学件的方法，对应复用代码如下:

- JobSelector 通过训练分类器为不同的数据选择不同的学件进行预测
```python
from learnware.reuse import JobSelectorReuser
reuse_job_selector = JobSelectorReuser(learnware_list=learnware_list) # learnware_list 是已载入的学件 list
predict_y = reuse_job_selector.predict(user_data=test_x) # test_x 是用户任务的特征数据，predict_y 复用学件预测得到的标签
```

- Averaging 使用平均集成的方法进行预测，其中`mode`的值`vote_by_label`表示对分类任务使用大多数投票集成
```python
from learnware.reuse import AveragingReuser
reuse_ensemble = AveragingReuser(learnware_list=learnware_list, mode="vote_by_label")
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)
```

更具体使用方法和原理请参考 [link]。

### 使用有标记数据复用学件

额外使用有标记的验证集数据，可以通过 `EnsemblePruning` 方法复用学件。`EnsemblePruning` 方法根据有标记的验证数据通过选择性集成的方法集成适合用户任务的学件并进行预测，代码如下：

```python
from learnware.reuse import EnsemblePruningReuser
reuse_ensemble_pruning = EnsemblePruningReuser(learnware_list=learnware_list) 
reuse_ensemble_pruning.fit(val_X=val_X, val_y=val_y) # (val_X, val_y) 是有标记的验证集数据
predict_y = reuse_job_selector.predict(user_data=test_x) 
```

更具体使用方法和原理请参考 [link]。


## 异构学件复用方法

对应异构学件，（待填）
