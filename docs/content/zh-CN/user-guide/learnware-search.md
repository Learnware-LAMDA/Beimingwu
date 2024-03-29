# 如何查搜学件？

在北冥坞系统中，学件既可以通过网页端查搜，也可以使用 `learnware` Python 包进行查搜。

接下来，我们将分别对这两种方式进行介绍。


## 通过网页端查搜

### 常规查搜

点击网站导航栏处的「[查搜](https://www.bmwu.cloud/#/search)」按钮，即可开始学件查搜。

系统支持通过语义规约进行学件查搜，也可以通过上传统计规约进行查搜，还可以将两种查搜方式结合到一起。

- **语义规约查搜**：支持通过学件名称搜索和通过标签搜索；查搜时输入名称或者选择标签；
- **统计规约查搜**：支持通过表格、图像、文本数据的统计规约进行查搜；查搜时上传统计规约对应的 `json` 文件。

进行统计规约查搜时，各种数据类型对应的统计规约可以通过如下命令生成：

```python
from learnware.specification import generate_stat_spec

data_type = "table" # 数据类型范围: ["table", "text", "image"]
stat_spec = generate_stat_spec(type=data_type, X=train_x)
stat_spec.save("stat.json")
```

查搜完成后，系统将显示单学件的查搜结果，在部分情况下，系统还会显示多学件组合的查搜结果。您可以根据需求下载相应的学件（组）。

### 异构表格查搜

对于表格数据，常规查搜仅能在特征空间维度相同的学件中进行查搜，当学件基座系统中没有维度相匹配的学件时，常规查搜将返回空结果。当您提交的为表格类型的统计规约，页面将弹出提示，提醒您可以开启异构查搜。

#### 如何开启异构查搜？

异构表格查搜需要您额外提供每一个特征维度的语义信息，这一过程可以通过手动填写或者直接上传维度语义信息的 `json` 文件，语义信息的 `json` 文件格式如下：

```json
{
    "Dimension": 2,
    "Description": {
        "0": "This is a description of 0-th feature", 
        "1": "This is a description of 1-th feature"
    }
}
```
请确保语义信息中的「Dimension」、「Description 中的维度范围」以及「统计规约的特征维度」是**一致**的，否则异构功能将无法正常开启。当您未指定任务类型时，市场会返回所有潜在有帮助的分类和回归学件，而当您指定“分类”或者“回归”任务时，市场会返回相应类型的学件。

值得注意的是，推荐的特征空间不同的模型无法在您的任务上直接进行预测，请参考「[学件部署](/zh-CN/user-guide/learnware-deploy)」页面的指南进行异构表格学件的部署。


## 通过 learnware 包查搜

网页端外，`learnware` 包也提供学件查搜的接口，首先需要登录：

```python
from learnware.client import LearnwareClient

# Login to Beiming system
client = LearnwareClient()
client.login(email="your email", token="your token")
```

其中 email 为系统的注册邮箱，token 为访问学件 API 的令牌，可在网页端「个人信息 - 客户端令牌」处生成。 



### 常规查搜

与网页端查搜相对应，learnware 包也支持语义规约查搜、统计规约查搜、语义规约 + 统计规约的混合查搜。

您可以通过语义规约在学件基座系统中查搜学件，所有符合语义规约的学件都将通过 API 返回。例如，下列代码将得到系统中所有任务类型为分类的学件：

```python
from learnware.market import BaseUserInfo
from learnware.specification import generate_semantic_spec

user_semantic = generate_semantic_spec(
    task_type="Classification"
)
user_info = BaseUserInfo(semantic_spec=user_semantic)
search_result = client.search_learnware(user_info)
```
上述代码中 `search_result` 为 dict 类型，具体结构如下（`"single"` 和 `"multiple"` 分别对应单学件和多学件的查搜结果）：
```python
search_result = {
    "single": {
        "learnware_ids": List[str],
        "semantic_specifications": List[dict],
        "matching": List[float],
    },
    "multiple": {
        "learnware_ids": List[str],
        "semantic_specifications": List[dict],
        "matching": float,
    },
}
```

您也可以通过统计规约在学件基座系统中查搜学件，这些模型往往具有更好的针对性，并将通过 API 返回。利用上述提到的 `generate_stat_spec` 函数，您可以生成当前任务的统计规约 `stat_spec`，随后使用下列代码获取系统中符合该统计规约的同数据类型的学件：

```python
user_info = BaseUserInfo(stat_info={stat_spec.type: stat_spec})
search_result = client.search_learnware(user_info)
```

通过将统计规约和语义规约结合起来，您可以进行更加细致的查搜。例如，以下代码演示了如何在表格型学件中查搜同时满足您任务语义规约和统计规约的学件：

```python
user_semantic = generate_semantic_spec(
    task_type="Classification",
    scenarios=["Business"],
)
rkme_table = generate_stat_spec(type="table", X=train_x)
user_info = BaseUserInfo(
    semantic_spec=user_semantic, stat_info={rkme_table.type: rkme_table}
)
search_result = client.search_learnware(user_info)
```

当学件查搜完成后，您可以通过 `search_result` 中的学件 ID 本地加载和使用学件：

```python
learnware_id = search_result["single"]["learnware_ids"][0]
learnware = client.load_learnware(
    learnware_id=learnware_id, runnable_option="conda"
)
# test_x is the user's data for prediction
predict_y = learnware.predict(test_x)
```

更详细的部署指南可查看：[学件部署](/zh-CN/user-guide/learnware-deploy)。


### 异构表格查搜

对于表格型任务，如果任务类型为“分类”或者回归，并且您提供了统计规约、在语义规约中包含了每个维度特征的语义描述，系统会自动启动异构表格查搜，以匹配和推荐特征空间不对齐的模型。以下代码示例展示了如何通过 API 执行异构表格查搜：

```python
input_description = {
    "Dimension": 2,
    "Description": {
        "0": "leaf width",
        "1": "leaf length",
    },
}
user_semantic = generate_semantic_spec(
    task_type="Classification",
    scenarios=["Business"],
    input_description=input_description,
)
rkme_table = generate_stat_spec(type="table", X=train_x)
user_info = BaseUserInfo(
    semantic_spec=user_semantic, stat_info={rkme_table.type: rkme_table}
)
search_result = client.search_learnware(user_info)
```