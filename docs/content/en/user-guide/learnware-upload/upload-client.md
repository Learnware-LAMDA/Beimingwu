# Upload Learnware via Client Interface

In the Beimingwu system, learnware can be uploaded either through the web interface or by using the learnware Python package, which means uploading via a client.

Next, we will introduce how to upload using the learnware package, starting with the need to log in:
```python
from learnware.client import LearnwareClient, SemanticSpecificationKey

# Login to the Beimingwu system
client = LearnwareClient()
client.login(email="your email", token="your token")
```

Where "email" is your registered email address in the system, and "token" is the token for accessing the learnware API, which can be generated in the web interface under "Personal Information - Client Token."

## Prepare Semantic Specification

After successfully logging in, you need to prepare the semantic specification. Here is an example of a "Table Data" for a "Classification Task":

```python
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

Additionally, it's important to note:
- If "data_type" is `"Table"`, you need to specify the semantics of each dimension of the model's input data to make the uploaded learnware suitable for tasks with heterogeneous feature spaces.
- If "task_type" is `"Classification"`, you need to provide the semantics of model output labels (prediction labels start from 0), making the uploaded learnware suitable for classification tasks with heterogeneous output spaces.
- If "task_type" is `"Regression"`, you need to specify the semantics of each dimension of the model output, making the uploaded learnware suitable for regression tasks with heterogeneous output spaces.

## Upload Learnware

Finally, fill in the semantic specification and the path to the learnware zip package to complete the learnware upload.

The preparation of the learnware zip package can be referred to: [How to Prepare a Learnware?](/en/user-guide/learnware-upload/prepare)

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

After uploading, the backend will perform a check on the learnware. Once the check passes, the learnware's tag will change to "SUCCESS", and your uploaded learnware will appear in the system.