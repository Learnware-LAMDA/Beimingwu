# How to Deploy and Reuse Learnware?

In the Beiming system, users can deploy and reuse learnwares using the `learnware` Python package.

## Loading Learnware and Environments

Users can load learnwares using the `LearnwareClient` class from the `learnware` Python package. First, instantiate a `LearnwareClient`:

```python
from learnware.client import LearnwareClient
client = LearnwareClient()
```

### Loading Learnware by Learnware ID

Assuming the user knows the ID of the learnware they want to load, they can use the following code to load the corresponding learnware and its environment:

```python
learnware_id = "00000082"
learnware = client.load_learnware(
    learnware_id=learnware_id, runnable_option="docker"
)
```

When the user wants to load multiple learnwares according to the id list `learnware_ids`, it can be accomplished with the following code:
```python
learnware_ids = ["00000082", "00000120"]
learnware_list = client.load_learnware(
    learnware_id=learnware_ids, runnable_option="docker"
)
```

The `runnable_option` parameter includes three options (default is `None`), each corresponding to a specific learnware deployment method:

- `None`: Load only learnware specifications and basic information; run the learnware using the current `learnware` package's Python environment.
- `"conda"`: Install a separate `conda` virtual environment for each learnware (automatically deleted after execution); run each learnware independently within its virtual environment.
- `"docker"`: Install a `conda` virtual environment inside a Docker container (automatically destroyed after execution); run each learnware independently within the container (requires Docker privileges).

It's important to note that while the system makes every effort to ensure the security of each learnware, the `None` and `"conda"` modes are **not secure** if there are any malicious learnwares. If the user cannot guarantee the security of the learnware they want to load, it's recommended to use the **relatively secure** `"docker"` mode to load the learnware.

### Loading Learnware from a ZIP File

In addition to loading learnware by ID, users can also load a learnware from a zip file downloaded from the web frontend:

```python
learnware_path = "learnware.zip"
learnware = client.load_learnware(
    learnware_path=learnware_path, runnable_option="docker"
)
```

When the user wants to load multiple learnwares according to the zip path list `learnware_paths`, it can be achieved with the following code:
```python
learnware_paths = ["learnware1.zip", "learnware2.zip"]
learnware_list = client.load_learnware(
    learnware_path=learnware_paths, runnable_option="docker"
)
```

### Utilizing Learnware for Prediction

After loading the learnware as described above, you can directly call the `predict(X)` interface of the learnware to perform predictions. The specific code is as follows:
```python
# test_x is the user's data for prediction
# predict_y is the prediction result of the learnware
learnware = client.load_learnware(learnware_id=learnware_id)
predict_y = learnware.predict(test_x)
```

## Homogeneous Learnware Reuse Methods

In addition to using learnwares directly, users can further make predictions on unlabeled data using basic learnware reuse methods provided by the system.

There are two main categories of reuse methods: (1) data-free reusers which reuse learnwares directly and (2) data-dependent reusers which reuse learnwares with a small amount of labeled data.

### Data-Free Reusers

Two methods for direct reuse of learnwares are provided: `JobSelectorReuser` and `AveragingReuser`.

- `JobSelectorReuser` selects different learnwares for different data by training a classifier. Here's how to use it:

```python
from learnware.reuse import JobSelectorReuser

# learnware_list is the list of loaded learnware
reuse_job_selector = JobSelectorReuser(learnware_list=learnware_list)

# test_x is the user's data for prediction
# predict_y is the prediction result of the reused learnware
predict_y = reuse_job_selector.predict(user_data=test_x)
```

- `AveragingReuser` uses an ensemble method to make predictions. The `mode` parameter specifies the specific ensemble method:

```python
from learnware.reuse import AveragingReuser


# Regression tasks:
#   - mode="mean": average the learnware outputs.
# Classification tasks:
#   - mode="vote_by_label": majority vote for learnware output labels.
#   - mode="vote_by_prob": majority vote for learnware output label probabilities.
reuse_ensemble = AveragingReuser(
    learnware_list=learnware_list, mode="vote_by_label"
)
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)
```

For more detailed usage and explanations, please refer to the [Learnware Package Data-Free Reuse Methods Introduction](https://learnware.readthedocs.io/en/latest/components/learnware.html#direct-reuse-of-learnware).

### Data-Dependent Reusers

When users have a small amount of labeled data, the system provides two methods: `EnsemblePruningReuser` and `FeatureAugmentReuser` to help adapt the learnwares.

- `EnsemblePruningReuser` selects a subset of suitable learnwares using a multi-objective evolutionary algorithm and uses an average ensemble for prediction:

```python
from learnware.reuse import EnsemblePruningReuser

# mode="regression": Suitable for regression tasks
# mode="classification": Suitable for classification tasks
reuse_ensemble_pruning = EnsemblePruningReuser(
    learnware_list=learnware_list, mode="regression"
)

# (val_X, val_y) is the small amount of labeled data
reuse_ensemble_pruning.fit(val_X=val_X, val_y=val_y)
predict_y = reuse_job_selector.predict(user_data=test_x)
```

- `FeatureAugmentReuser` enhances user task features by incorporating predictions from learnwares, subsequently training a simple model (logistic regression for classification tasks and ridge regression for regression tasks):

```python
from learnware.reuse import FeatureAugmentReuser

# mode="regression": Suitable for regression tasks
# mode="classification": Suitable for classification tasks
augment_reuser = FeatureAugmentReuser(
    learnware_list=learnware_list, mode="regression"
)

# (val_X, val_y) is the small amount of labeled data
augment_reuser.fit(val_X, val_y)
predict_y = augment_reuser.predict(user_data=test_x)
```

For more detailed usage and explanations, please refer to the [Learnware Package Data-Dependent Reuse Methods Introduction](https://learnware.readthedocs.io/en/latest/components/learnware.html#reuse-learnware-with-labeled-data).

## Heterogeneous Learnware Reuse Methods

The system provides the `HeteroMapAlignLearnware` class to help align heterogeneous learnware with the user's task, including two steps: input space alignment and output space alignment.

During the alignment process of heterogeneous learnware, the statistical specifications of the learnware and the user's task `(user_spec)` are used for input space alignment, and a small amount of labeled data `(val_x, val_y)` is used for output space alignment. Here's the code:

```python
from learnware.reuse import HeteroMapAlignLearnware

# mode="regression": For user tasks of regression
# mode="classification": For user tasks of classification
hetero_learnware = HeteroMapAlignLearnware(learnware=leanrware, mode="regression")
hetero_learnware.align(user_spec, val_x, val_y)

# Make predictions using the aligned heterogeneous learnware
predict_y = hetero_learnware.predict(user_data=test_x)
```

If you want to reuse multiple heterogeneous learnwares, you can combine `HeteroMapAlignLearnware` with the homogeneous reuse methods `AveragingReuser` and `EnsemblePruningReuser` as mentioned before:

```python
hetero_learnware_list = []
for learnware in learnware_list:
    hetero_learnware = HeteroMapAlignLearnware(learnware, mode="regression")
    hetero_learnware.align(user_spec, val_x, val_y)
    hetero_learnware_list.append(hetero_learnware)
            
# Reuse multiple heterogeneous learnwares using AveragingReuser
reuse_ensemble = AveragingReuser(learnware_list=hetero_learnware_list, mode="mean")
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)

# Reuse multiple heterogeneous learnwares using EnsemblePruningReuser
reuse_ensemble = EnsemblePruningReuser(
    learnware_list=hetero_learnware_list, mode="regression"
)
reuse_ensemble.fit(val_x, val_y)
ensemble_pruning_predict_y = reuse_ensemble.predict(user_data=test_x)
```