Material Two Translation:

# How to Upload Learnware?

In the Beimingwu system, you can upload a learnware both from the web interface and by using the `learnware` Python package.

Next, we will introduce two methods separately.

## Uploading through the Web Interface

Click the "Submit" button on the website's navigation bar at [Submit](https://www.lamda.nju.edu.cn/learnware/#/submit) to begin the process of uploading learnware.

The entire process is divided into the following 4 steps:
1. Fill in the name of the learnware.
2. Select tags for the learnware.
3. Provide a description for the learnware.
4. Upload the prepared learnware zip package.

The first three steps can be completed following the instructions on the website's pages, and the details for the fourth step can be found here: [How to Prepare Learnware](/zh-CN/user-guide/learnware-upload/prepare).

It's important to note that during the second step, "Select Tags":
- If the data type is "Table," you need to specify the semantics of each dimension of the model's input data to make the uploaded learnware suitable for tasks with heterogeneous feature spaces.
- If the task type is "Classification" or "Regression," you need to specify the semantics of each dimension of the model's output to make the uploaded learnware suitable for tasks with heterogeneous output spaces.

If there are many dimensions, consider using a large language model to analyze the feature engineering code and generate semantics for each dimension.

## Uploading using the learnware Package

Apart from the web interface, the learnware package also provides an interface for uploading learnware. First, you need to log in:

```python
from learnware.client import LearnwareClient, SemanticSpecificationKey

# Login to the Beimingwu system
client = LearnwareClient()
client.login(email="your email", token="your token")
```

Where "email" is your registered email address in the system, and "token" is the token for accessing the learnware API, which can be generated in the web interface under "Personal Information - Client Token."

Next, you need to prepare semantic specifications, here is an example of a "Table Data" for a "Classification Task":

```python
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
    description="Just an example for uploading learnware",
    data_type="Table",
    task_type="Classification",
    library_type="Scikit-learn",
    scenarios=["Business", "Financial"],
    input_description=input_description,
    output_description=output_description,
)
```

Please ensure that the input for semantic specification falls within the range given by `client.list_semantic_specification_values(key)`:
- "data_type" must be within `key=SemanticSpecificationKey.DATA_TYPE`.
- "task_type" must be within `key=SemanticSpecificationKey.TASK_TYPE`.
- "library_type" must be within `key=SemanticSpecificationKey.LIBRARY_TYPE`.
- "scenarios" must be a subset of `key=SemanticSpecificationKey.SENARIOS`.
- When "data_type" is "Table," you need to provide "Input Description."
- When "task_type" is in `["Classification", "Regression"]`, you need to provide "Output Description."

Finally, fill in the semantic specification and the path to the learnware zip package to complete the learnware upload.

Before uploading, remember to validate your learnware. Here's an example code:

```python
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

Once your learnware is successfully uploaded, you can find it under "Personal Information - My Learnware."

After uploading, the backend will perform a check on the learnware. You can check the validation status by clicking on the learnware. Once the check passes, the "Unverified" label will disappear, and your uploaded learnware will appear in the learnware.