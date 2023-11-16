# How to Deploy and Reuse Learnware?

In the Beiming system, users can deploy and reuse learnwares using the `learnware` Python package.

## Loading Learnware and Environments

Users can load learnware using the `LearnwareClient` class from the `learnware` Python package. First, define a `LearnwareClient`:

```python
from learnware.client import LearnwareClient
client = LearnwareClient()
```

### Loading Learnware by Learnware ID

Assuming the user knows the `id` of the learnware they want to load, they can use the following code to load the corresponding learnware and its environment:

```python
learnware_id = "00000082"
learnware_list = client.load_learnware(
    learnware_id=learnware_id, runnable_option="docker"
)
```

The `runnable_option` parameter has four options, each corresponding to one of the following ways to load learnware environments:

- `None`: Load only learnware specifications and basic information; the learnware cannot run at this stage.
- `"normal"`: Do not install a separate environment; run the learnware using the current `learnware` package's Python environment.
- `"conda_env"`: Install a separate `conda` virtual environment for each learnware (automatically deleted after execution); run each learnware independently within its virtual environment.
- `"docker"`: Install a `conda` virtual environment inside a Docker container (automatically destroyed after execution); run each learnware independently within the container (requires Docker privileges).

It's important to note that while the system makes every effort to ensure the security of each learnware, the `"normal"` and `"conda_env"` modes are **not secure** if there are any malicious learnwares. If the user cannot guarantee the security of the learnware they want to load, it's recommended to use the `"docker"` mode to load the learnware.

### Loading Learnware from a ZIP File

In addition to loading learnware by ID, users can also load learnware from a `zip` file downloaded from the web:

```python
learnware_path = "learnware1.zip"
learnware_list = client.load_learnware(
    learnware_path=learnware_path, runnable_option="docker"
)
```

## Homogeneous Learnware Reuse Methods

In addition to using learnware directly, users can further make predictions on unlabeled data using learnware reuse methods provided by the system.

There are two main categories of reuse methods: (1) direct reuse and (2) reuse based on a small amount of labeled data.

### Direct Reuse of Learnware

Two methods for direct reuse of learnware are provided: `JobSelector` and `Averaging`.

- `JobSelector` selects different learnwares for different data by training a classifier. Here's how to use it:

```python
from learnware.reuse import JobSelectorReuser

# learnware_list is the list of loaded learnware
reuse_job_selector = JobSelectorReuser(learnware_list=learnware_list)

# test_x is the user's data for prediction, predict_y is the prediction result of the reused learnware
predict_y = reuse_job_selector.predict(user_data=test_x)
```

- `Averaging` uses an ensemble method to make predictions. The `mode` parameter specifies the specific ensemble method:

```python
from learnware.reuse import AveragingReuser

# mode="mean": Suitable for regression tasks, averages the learnware outputs.
# mode="vote_by_label": Suitable for classification tasks, uses majority voting for learnware output labels.
# mode="vote_by_prob": Suitable for classification tasks, uses majority voting for learnware output label probabilities.
reuse_ensemble = AveragingReuser(
    learnware_list=learnware_list, mode="vote_by_label"
)
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)
```

For more detailed usage and explanations, please refer to the [Learnware Package Reuse Methods Introduction](#).

### Reusing Learnware with Labeled Data

When users have a small amount of labeled data, the system provides two methods: `EnsemblePruning` and `FeatureAugmentReuser` to help reuse learnwares.

- `EnsemblePruning` selectively integrates learnwares to choose the ones that are most suitable for the user's task:

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

For more detailed usage and explanations, please refer to the [Learnware Package Reuse Methods Introduction](#).

- `FeatureAugmentReuser` helps users reuse learnwares by augmenting features. The output of the original learnware is concatenated with the user's task features, and a simple model is trained on the labeled data (logistic regression for classification tasks and ridge regression for regression tasks):

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

## Heterogeneous Learnware Reuse Methods

The system provides the `HeteroMapAlignLearnware` class to help align heterogeneous learnware with the user's task, including two steps: input space alignment and output space alignment.

During the alignment process of heterogeneous learnware, the statistical specifications of the learnware and the user's task (`user_spec`) are used for input space alignment, and a small amount of labeled data (`(val_x, val_y)`) is used for output space alignment. Here's the code:

```python
from learnware.reuse import HeteroMapAlignLearnware

# mode="regression": For user tasks of regression
# mode="classification": For user tasks of classification
hetero_learnware = HeteroMapAlignLearnware(learnware=leanrware, mode="regression")
hetero_learnware.align(user_spec, val_x, val_y)

# Make predictions using the aligned heterogeneous learnware
predict_y = hetero_learnware.predict(user_data=test_x)
```

If you want to reuse multiple heterogeneous learnwares, you can combine `HeteroMapAlignLearnware` with the homogeneous reuse methods `Averaging` and `EnsemblePruning` as mentioned before:

```python
hetero_learnware_list = []
for learnware in learnware_list:
    hetero_learnware = HeteroMapAlignLearnware(learnware, mode="regression")
    hetero_learnware.align(user_spec, val_x, val_y)
    hetero_learnware_list.append(hetero_learnware)
            
# Reuse multiple heterogeneous learnwares using AveragingReuser
reuse_ensemble = A

veragingReuser(learnware_list=hetero_learnware_list, mode="mean")
ensemble_predict_y = reuse_ensemble.predict(user_data=test_x)

# Reuse multiple heterogeneous learnwares using EnsemblePruningReuser
reuse_ensemble = EnsemblePruningReuser(
    learnware_list=hetero_learnware_list, mode="regression"
)
reuse_ensemble.fit(val_x, val_y)
ensemble_pruning_predict_y = reuse_ensemble.predict(user_data=test_x)
```