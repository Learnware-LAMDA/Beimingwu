# 如何上传学件？

在北冥坞系统中，学件既可以从网页端上传，也可以使用 `learnware` Python 包进行上传。

接下来，我们将分别对这两种方式进行介绍。

## 通过网页端上传

点击网站导航栏处的「[提交](https://www.lamda.nju.edu.cn/learnware/#/submit)」按钮，即可开始学件上传。

整个流程分为以下 4 步：
1. 填写学件的名称
2. 选择学件的标签
3. 填写学件的描述
4. 上传准备好的学件 zip 包

其中前 3 步可根据网站页面指引进行操作，第 4 步可具体查看：[如何准备一个学件？](/zh-CN/user-guide/learnware-upload/prepare)

需要注意的是，在第 2 步「选择标签」的过程中：
- 如果数据类型为「表格」，则需要填写模型输入数据的每一维特征语义，使上传的学件可用于异构特征空间的任务；
- 如果任务类型为「分类」或「回归」，则需要填写模型输出的每一维语义，使上传的学件可用于异构输出空间的任务。

如果维度过多，可考虑使用大语言模型。通过分析特征工程的代码，生成各维度的语义。


## 使用 learnware 包上传

除网页端外，learnware 包也提供学件上传的接口，首先需要登录：
```py
from learnware.client import LearnwareClient, SemanticSpecificationKey

# Login to Beiming system
client = LearnwareClient()
client.login(email="your email", token="your token")
```
其中 email 为系统的注册邮箱，token 为访问学件 API 的令牌，可在网页端「个人信息 - 客户端令牌」处生成。
随后需要准备语义规约，此处以「表格数据」的「分类任务」为例：
```py
# Prepare input description when data_type="Table"
input_description = {
    "Dimension": 5,
    "Description": {
        "0": "age",
        "1": "weight",
        "2": "body length",
        "3": "animal type",
        "4": "claw length"
    },
}

# Prepare output description when task_type in ["Classification", "Regression"]
output_description = {
    "Dimension": 3,
    "Description": {
        "0": "the probability of being a cat",
        "1": "the probability of being a dog",
        "2": "the probability of being a bird",
    },
}

# Create semantic specification
semantic_spec = client.create_semantic_specification(
    name="learnware_example",
    description="Just a example for uploading a learnware",
    data_type="Table",
    task_type="Classification",
    library_type="Scikit-learn",
    scenarios=["Business", "Financial"],
    input_description=input_description,
    output_description=output_description,
)
```
请确保语义规约的输入在 `client.list_semantic_specification_values(key)` 给出的范围内：
- data\_type 必须在 `key=SemanticSpecificationKey.DATA_TYPE` 对应的结果中；
- task\_type 必须在 `key=SemanticSpecificationKey.TASK_TYPE` 对应的结果中；
- library\_type 必须在 `key=SemanticSpecificationKey.LIBRARY_TYPE` 对应的结果中；
- scenarios 必须为 `key=SemanticSpecificationKey.SENARIOES` 对应结果的子集；
- 当 data\_type 为 `"Table"` 时，需要填写「输入描述」；
- 当 task\_type 在 `["Classification", "Regression"]` 中时，需要填写「输出描述」。

最后，填写语义规约和学件 zip 包路径，即可实现学件上传。

记得在上传前先对学件进行验证，代码示例如下：
```py
# Prepare your learnware zip file
zip_path = "your learnware zip"

# Check your learnware before upload
client.check_learnware(
    learnware_zip_path=zip_path, semantic_specification=semantic_spec
)

# Upload your learnware
learnware_id = client.upload_learnware(
    learnware_zip_path=zip_path, semantic_specification=semantic_spec
)
```

学件上传成功后，可以在「个人信息 - 我的学件」处看到上传的学件。

学件上传后，后台会对学件进行检查。点击学件，可在「验证状态」处查看。检查通过后，学件的 `Unverified` 标签会消失，且上传的学件会在系统中出现。