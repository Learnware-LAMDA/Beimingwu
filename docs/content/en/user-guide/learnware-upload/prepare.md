# How to Prepare a Learnware?

In the Beimingwu system, each learnware is a `zip` package, which should contain at least the following four files:

- `learnware.yaml`: learnware configuration file.
- `__init__.py`: methods for using the model.
- `stat.json`: the statistic specification of the learnware. Its filename can be customized and recorded in learnware.yaml.
- `environment.yaml` or `requirements.txt`: specifies the environment for the model.

When creating these four files, you need to use the `learnware` Python package. You can find specific installation instructions here: [Installation Guide](/en/overview/installation).

To facilitate the construction of learnware, we provide a [learnware template](http://www.lamda.nju.edu.cn/learnware/static/learnware-template.zip) that you can use as a basis for building your own learnware.

Next, we will provide detailed explanations for the content of these four files.

## Model Invocation File `__init__.py`

To ensure that the uploaded learnware can be used by subsequent users, you need to provide interfaces for model fitting, prediction, and fine-tuning in `__init__.py`. Among these interfaces, only the `predict` interface is mandatory, while the others depend on the functionality of your model. Here is a template format for the `__init__.py` file:

```py
import os
import pickle
import numpy as np
from learnware.model import BaseModel

class MyModel(BaseModel):
    def __init__(self):
        super(MyModel, self).__init__(input_shape=(37,), output_shape=(1,))
        dir_path = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(dir_path, "model.pkl")
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.model = self.model.fit(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X)

    def finetune(self, X: np.ndarray, y: np.ndarray):
        pass
```

Please note that the `MyModel` class should inherit from `BaseModel` in the `learnware.model` module, and the class name (e.g., MyModel) should be specified in the learnware.yaml file later. Also, if you need to import other modules from the zip package in `__init__.py`, use relative imports. For example:

```py
from .package_name import *
from .package_name import module_name
```

## Learnware Statistic Specification `stat.json`

A learnware consists of a model and a specification. Therefore, after preparing the model, you need to generate a statistic specification for it. Specifically, using the previously installed `learnware` package, you can use the training data `train_x` (supported types include numpy.ndarray, pandas.DataFrame, and torch.Tensor) as input to generate the statistic specification of the model.

Here is an example of the code:

```py
from learnware.specification import generate_stat_spec

data_type = "table" # Data types: ["table", "image", "text"]
spec = generate_stat_spec(type=data_type, X=train_x)
spec.save("stat.json")
```

It's worth noting that the above code only runs on your local computer and does not interact with any cloud servers or leak any local private data.

## Learnware Configuration File `learnware.yaml`

This file is used to specify the class name (`MyModel`) in the model invocation file `__init__.py`, the module called for generating the statistic specification (`learnware.specification`), the category of the statistic specification (`RKMEStatSpecification`), and the specific filename (`stat.json`):

```yaml
model:
  class_name: MyModel
  kwargs: {}
stat_specifications:
  - module_path: learnware.specification
    class_name: RKMEStatSpecification
    file_name: stat.json
    kwargs: {}
```

Please note that the statistic specification class name `RKMEStatSpecification` for different data types `["table", "image", "text"]` is `[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification]`, respectively.

## Model Runtime Dependencies `environment.yaml`

To ensure that your uploaded learnware can be used by other users, the `zip` package of the uploaded learnware should specify the model's runtime dependencies. It is recommended to provide an `environment.yaml` file that supports `conda`. You can export this file directly from the `conda` virtual environment using the following command:

- For Linux and macOS systems:

```bash
conda env export | grep -v "^prefix: " > environment.yaml
```

- For Windows systems:

```bash
conda env export | findstr /v "^prefix: " > environment.yaml
```

Note that the `environment.yaml` file in the `zip` package needs to be encoded in `UTF-8` format. Please check the encoding format of the `environment.yaml` file after using the above command. Due to the `conda` version and system differences, you may not get a `UTF-8` encoded file (e.g. get a `UTF-16LE` encoded file). You'll need to manually convert the file to `UTF-8`, which is supported by most text editors. The following `Python` code for encoding conversion is also for reference:

```python
import codecs

# Read the output file from the 'conda env export' command
# Assuming the file name is environment.yaml and the export format is UTF-16LE
with codecs.open('environment.yaml', 'r', encoding='utf-16le') as file:
    content = file.read()

# Convert the content to UTF-8 encoding
output_content = content.encode('utf-8')

# Write to UTF-8 encoded file
with open('environment.yaml', 'wb') as file:
    file.write(output_content)
```

Alternatively, you can provide a `requirements.txt` file that supports `pip`. This file should list the packages required for running the `__init__.py` file and their specific versions. You can obtain these version details by executing the `pip show <package_name>` or `conda list <package_name>` command. Here is an example file:

```txt
learnware==0.1.0.999
numpy==1.23.5
scikit-learn==1.2.2
```

Manually listing these dependencies can be cumbersome, so you can also use the `pipreqs` package to automatically scan your entire project and export the packages used along with their specific versions (though some manual verification may be required):

```bash
pip install pipreqs
pipreqs ./  # Run this command in the project's root directory
```

Regardless of which method you use, try to remove unnecessary dependencies to minimize the number of required dependencies.

## Local Validation of Learnware

After filling in the above files, you can proceed to upload your learnware. Once the learnware is successfully uploaded, the system backend will automatically add it to the validation queue to check whether the learnware meets the requirements, including the format of the learnware and whether the model can be run. This validation process may take some time, depending on the complexity of the learnware and the workload of the system backend. The validation results will be displayed on the website.

Since the backend validation of learnware can be time-consuming, we recommend that you validate your learnware locally before uploading it by using the following code:

```py
from learnware.client import LearnwareClient

zip_path = "learnware.zip"  # Path to the learnware zip package to be validated
LearnwareClient.check_learnware(zip_path)
```

After successfully passing the local validation, you can proceed to upload the learnware to the system to improve the efficiency of the validation process.
