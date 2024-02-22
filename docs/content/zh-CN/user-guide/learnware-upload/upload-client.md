# 通过客户端上传学件

在北冥坞系统中，学件既可以从网页端上传，也可以使用 `learnware` Python 包进行上传，即使用客户端上传。

接下来，我们将介绍如何使用 `learnware` 包上传学件。首先需要登录：
```py
from learnware.client import LearnwareClient, SemanticSpecificationKey

# Login to Beiming system
client = LearnwareClient()
client.login(email="your email", token="your token")
```
其中 email 为系统的注册邮箱，token 为访问学件 API 的令牌，可在网页端「个人信息 - 客户端令牌」处生成。

## 准备语义规约

成功登录后，您需要准备语义规约，此处以「表格数据」的「分类任务」为例：
```py
from learnware.specification import generate_semantic_spec

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
        "0": "cat",
        "1": "dog",
        "2": "bird",
    },
}

# Create semantic specification
semantic_spec = generate_semantic_spec(
    name="learnware_example",
    description="Just a example for uploading a learnware",
    data_type="Table",
    task_type="Classification",
    library_type="Scikit-learn",
    scenarios=["Business", "Financial"],
    license=["Apache-2.0"],
    input_description=input_description,
    output_description=output_description,
)
```
请确保语义规约的输入在 `client.list_semantic_specification_values(key)` 给出的范围内：
- data\_type 必须在 `key=SemanticSpecificationKey.DATA_TYPE` 对应的结果中；
- task\_type 必须在 `key=SemanticSpecificationKey.TASK_TYPE` 对应的结果中；
- library\_type 必须在 `key=SemanticSpecificationKey.LIBRARY_TYPE` 对应的结果中；
- scenarios 必须为 `key=SemanticSpecificationKey.SENARIOES` 对应结果的子集。

另外，需要注意：
- 如果 data\_type 为 `"Table"`，则需要填写模型输入数据的每一维特征语义，使上传的学件可用于特征空间不对齐的任务；
- 如果 task\_type 为 `"Classification"`，则需要填写模型输出标记的语义（预测标记从 0 开始编号），使上传的学件可用于输出空间不对齐的分类任务；
- 如果 task\_type 为 `"Regression"`，则需要填写模型输出的每一维语义，使上传的学件可用于输出空间不对齐的回归任务；

## 学件上传

接下来，填写语义规约和学件 zip 包路径，您即可完成学件上传。

关于学件 zip 包的准备，请参考指南：[如何准备一个学件？](/zh-CN/user-guide/learnware-upload/prepare)。 在上传前，建议您先对学件进行本地验证，代码示例如下：

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

学件上传后，您可以在「个人信息 - 我的学件」页面看到上传的学件。系统后台会自动将该学件加入验证队列，以检验学件是否符合规范。如果学件通过验证，其标签会变为「验证成功」，并出现在系统中。