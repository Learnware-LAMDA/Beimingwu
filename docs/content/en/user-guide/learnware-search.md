# How to Search for Learnwares?

In the Beimingwu system, you can search for learnwares through the web interface or the `learnware` package.

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

You can search for learnwares in the learnware dock system through semantic specifications, and all learnwares that meet the semantic specifications will be returned via the API. For example, the following code retrieves all learnware in the system with a task type of "Classification":

```python
user_semantic = client.create_semantic_specification(
    task_type="Classification"
)
specification = Specification()
specification.update_semantic_spec(user_semantic)
learnware_list = client.search_learnware(specification, page_size=None)
```

You can also search for learnwares in the learnware dock system through statistical specifications, and all learnwares with similar distribution will be returned through the API. By using the `generate_stat_spec` function mentioned above, you can easily obtain the statistical specification `stat_spec` corresponding to your current task. Then, you can use the following code to retrieve learnwares in the system that satisfies the statistical specification for the same type of data as your task:

```python
specification = Specification()
specification.update_stat_spec(stat_spec)
learnware_list = client.search_learnware(specification, page_size=None)
```

By combining both semantic and statistical specifications, you can perform more accurate searches. For example, the following code searches for learnware in tabular data that meet both semantic and statistical specifications:

```python
user_semantic = client.create_semantic_specification(
    task_type="Classification",
    scenarios=["Business"],
)
data_type = "table"
rkme_table = generate_stat_spec(type=data_type, X=train_x)

specification = Specification()
specification.update_semantic_spec(user_semantic)
specification.update_stat_spec(rkme_table)
learnware_list = client.search_learnware(specification, page_size=None)
```

Once the learnware search is complete, you can use the following code to download the learnware and configure the environment:

```python
for temp_learnware in learnware_list:
    learnware_id = temp_learnware["learnware_id"]

    # you can use the learnware to make predictions now
    learnware = client.load_learnware(
        learnware_id=learnware_id, runnable_option="conda"
    )
```

For more detailed deployment guidance, you can refer to the "[Learnware Deployment](/en/user-guide/learnware-deploy)" page.

### Heterogeneous Table Search

When you provide a statistical specification for tabular data, the task type is "Classification" or "Regression," and your semantic specification includes descriptions for each dimension, the system will automatically enable heterogeneous table search. It won't only search in the tabular learnwares with same dimensions. The following code will perform heterogeneous table search through the API:

```python
input_description = {
    "Dimension": 2,
    "Description": {
        "0": "leaf width",
        "1": "leaf length",
    },
}
user_semantic = client.create_semantic_specification(
    task_type="Classification",
    scenarios=["Business"],
    input_description=input_description,
)
data_type = "table"
rkme_table = generate_stat_spec(type=data_type, X=train_x)

specification = Specification()
specification.update_semantic_spec(user_semantic)
specification.update_stat_spec(rkme_table)
learnware_list = client.search_learnware(specification, page_size=None)
```