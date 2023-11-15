# How to Search for Learnware?

In the Beimingwu system, you can search for learnware through both the web interface and by using the `learnware` Python package.

Next, we will introduce these two methods separately.

## Searching through the Web Interface

### Regular Search

Click on the "Search" button in the website's navigation bar at "[Search](https://www.lamda.nju.edu.cn/learnware/#/search)," and you can initiate a learnware search.

The system supports learnware searches through semantic specifications or statistical specifications, and you can also combine these two search methods.

- Semantic Specification Search: You can search by learnware name or select tags when using this method.
- Statistical Specification Search: You can search by uploading a `json` file corresponding to the statistical specification of table, image, or text data.

To perform a statistical specification search, you can generate the specification for various data types using the following command:

```python
from learnware.specification import generate_stat_spec

data type = "table" # Data type options: ["table", "text", "image"]
spec = generate_stat_spec(type=data_type, X=train_x)
spec.save("stat.json")
```

After completing the search, the system will display the results for individual learnware searches, and in some cases, it may also show results for multiple learnware combinations. You can download the corresponding learnware (or group) based on your needs.

### Heterogeneous Table Search

For statistical specifications of table data, regular searches can only be performed within learnware with the same feature space dimensions. When there are no matching learnware with the same dimension in the learnware market, a regular search will return an empty list. In such cases, the page will prompt you to enable heterogeneous table search.

When you choose to enable heterogeneous table search, the system will require you to provide semantic information for each dimension. This can be done either by manual input or by uploading a `json` file with dimension semantics information. The `json` file format for semantic information is as follows:

```json
{
    "Dimension": 2,
    "Description": {
        "0": "This is a description of the 0-th feature", 
        "1": "This is a description of the 1-th feature"
    }
}
```

It is worth noting that recommended models with different feature spaces cannot directly predict tasks for your specific needs. Please refer to the "Learnware Deployment" page for guidance on deploying heterogeneous table learnware.

## Searching through the learnware Package

In addition to the web interface, the `learnware` package also provides an interface for searching for learnware. First, you need to log in as follows:

```python
from learnware.client import LearnwareClient

# Login to Beiming system
client = LearnwareClient()
client.login(email="your email", token="your token")
```

Where "email" is your registered email for the system, and "token" is the token for accessing the learnware API, which can be generated on the web interface under "Personal Information - Client Token."

### Regular Search

Similar to the web interface search, the `learnware` package supports semantic specification search, statistical specification search, and a combination of semantic and statistical specification searches.

You can search for learnware in the learnware market through semantic specifications, and all learnware that meet the semantic specifications will be returned via the API. For example, the following code retrieves all learnware in the market with a task type of "Classification":

```python
user_semantic = {
    "Task": {"Values": ["Classification"], "Type": "Class"},
}

specification = Specification()
specification.update_semantic_spec(user_semantic)
learnware_list = client.search_learnware(specification, page_size=None)
```

You can also search for learnware in the learnware market that satisfies your task's statistical specifications by using the `generate_rkme_image_spec`, `generate_rkme_spec`, and `generate_rkme_text_spec` functions mentioned earlier to obtain your current task's statistical specification `rkme_spec`. Then, use the following code to retrieve learnware in the same data type (e.g., table) that satisfy your task's statistical specifications:

```python
specification = Specification()
specification.update_stat_spec(rkme_spec)
learnware_list = client.search_learnware(specification, page_size=None)
```

By combining both semantic and statistical specifications, you can perform more detailed searches. For example, the following code searches for learnware in tabular data that meet both semantic and statistical specifications:

```python
user_semantic = {
    "Task": {"Values": ["Classification"], "Type": "Class"},
    "Scenario": {"Values": ["Business"], "Type": "Tag"},
}
rkme_table = generate_rkme_spec(table_feature)

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
        learnware_id=learnware_id, runnable_option="conda_env"
    )
```

For more detailed deployment guidance, you can refer to the "Learnware Deployment" page.