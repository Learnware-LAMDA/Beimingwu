# How to Search for Learnware(s)?

In the Beimingwu system, you can search for learnware(s) through the web interface or the `learnware` package.

Next, we will introduce these two methods separately.

## Searching through the Web Interface

### Regular Search

Click on the "Search" button in the website's navigation bar at "[Search](https://www.bmwu.cloud/#/search)," and you can start learnware search.

The system supports learnware search through semantic specifications or statistical specifications, and you can also combine these two search methods.

- **Semantic Specification Search**: You can search learnwares by descriptions or select tags when using this method.
- **Statistical Specification Search**: You can search learnwares by uploading a JSON file corresponding to the statistical specification of table, image, or text data.

To perform a statistical specification search, you can generate the specification for various data types using the following command:

```python
from learnware.specification import generate_stat_spec

data type = "table" # Data type options: ["table", "text", "image"]
stat_spec = generate_stat_spec(type=data_type, X=train_x)
stat_spec.save("stat.json")
```

After completing the search, the system will display the results for single learnwares, and in some cases, it may also show results for multiple learnware combinations. You can download the corresponding learnware (or group) based on your needs.

### Heterogeneous Table Search

For tabular data, regular search can only be conducted within learnwares with the same dimension of the feature space. When there are no learnwares with matching dimension in the learnware dock system, regular search will return an empty result. When you submit a statistical specification for tabular data, a message will appear on the page reminding you that you can enable heterogeneous search.

#### How to Enable Heterogeneous Search?

When you choose to enable heterogeneous table search, the system will require you to provide semantic information for each dimension. This can be done either by manually filling in or directly uploading a JSON file describing semantics information of each feature. The format of the JSON file is as follows:

```json
{
    "Dimension": 2,
    "Description": {
        "0": "This is a description of the 0-th feature", 
        "1": "This is a description of the 1-th feature"
    }
}
```

Please ensure that the "Dimension", the range of indices in "Description", and the dimensions of the statistical specification are consistent. Otherwise, the heterogeneous function cannot be properly enabled. 

It is worth noting that recommended models with different feature spaces cannot directly predict on your task. Please refer to the "[Learnware Deployment](/en/user-guide/learnware-deploy)" page for guidance about deploying heterogeneous table learnwares.

## Searching through the learnware Package

In addition to the web interface, the `learnware` package also provides an interface about searching for learnwares. First, you need to log in as follows:

```python
from learnware.client import LearnwareClient

# Login to Beiming system
client = LearnwareClient()
client.login(email="your email", token="your token")
```

Where "email" is your registered email for the system, and "token" is the token for accessing the learnware API, which can be generated on the web interface under "Personal Information - Client Token."

### Regular Search

Similar to the web interface search, the `learnware` package supports semantic specification search, statistical specification search, and a combination of semantic and statistical specification search.

You can search for learnware(s) in the learnware dock system through semantic specifications, and all learnwares that meet the semantic specifications will be returned via the API. For example, the following code retrieves all learnware in the system with a task type of "Classification":

```python
from learnware.market import BaseUserInfo
from learnware.specification import generate_semantic_spec

user_semantic = generate_semantic_spec(
    task_type="Classification"
)
user_info = BaseUserInfo(semantic_spec=user_semantic)
search_result = client.search_learnware(user_info)
```

In the above code, `search_result` is of type dict, with the following specific structure (`"single"` and `"multiple"` correspond to the search results for a single learnware and multiple learnwares, respectively):
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

Moreover, you can also search for learnware(s) in the learnware dock system through statistical specifications, and more targeted learnwares for your task will be returned through the API. Using the `generate_stat_spec` function mentioned above, you can generate your task's statistical specification `stat_spec`. Then, you can use the following code to easily obtain suitable learnware(s) identified by the system for your specific task:

```python
user_info = BaseUserInfo(stat_info={stat_spec.type: stat_spec})
search_result = client.search_learnware(user_info)
```

By combining both semantic and statistical specifications, you can perform more accurate searches. For instance, the code below demonstrates how to search for learnware(s) in tabular data that satisfy both the semantic and statistical specifications:

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

After the learnware search is completed, you can locally load and use the learnwares through the learnware IDs in `search_result`, as shown in the following example:

```python
learnware_id = search_result["single"]["learnware_ids"][0]
learnware = client.load_learnware(
    learnware_id=learnware_id, runnable_option="conda"
)
# test_x is the user's data for prediction
predict_y = learnware.predict(test_x)
```

For more detailed deployment guidance, you can refer to the "[Learnware Deployment](/en/user-guide/learnware-deploy)" page.

### Heterogeneous Table Search

For tabular tasks, if the task type is "Classification" or "Regression", and you have provided a statistical specification along with descriptions for each feature dimension in the semantic specification, the system will enable heterogeneous table search. This is designed to support searching models from different feature spaces preliminarily. The following code example shows how to perform a heterogeneous table search via the API:

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