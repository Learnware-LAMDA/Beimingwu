# Quick Start

Welcome to Beimingwu learnware dock system! The following content will help you quickly experience the system, mainly including learnware search and deployment.

## Learnware Search

In Beimingwu, learnwares can be searched using both semantic information and statistical information.

When searching with semantic information, you can fill in the information about your target learnware, and the system will search in the names and descriptions of learnwares. You can also filter by tags.

![image](../../public/quick-start/semantic-search-en.jpg)

When searching with statistical information, you need to generate and submit a statistical specification, which captures the data distribution while not disclosing your original data. Using the API we provided, you can easily generate this statistical specification locally.

```python
from learnware.specification import generate_stat_spec

data_type = "table"  # Data types: ["table", "image", "text"]
spec = generate_stat_spec(type=data_type, X=test_x)
spec.save("stat.json")
```

By uploading the JSON file containing statistical information, the system will match learnware with similar statistical information. You can download the learnware zip by clicking on the download button in the lower left corner of the learnware card.

![image](../../public/quick-start/stat-search-single-en.jpg)

In some cases, assembling multiple helpful learnwares may be more beneficial for your task. The system will accordingly recommend a combination of these learnwares as a package. You can download the package using the "Download All" button in the upper right corner.

![image](../../public/quick-start/stat-search-multiple-en.jpg)

## Learnware Deployment

After downloading learnware(s), your local environment may not be compatible with the downloaded learnware, but you can quickly deploy it using the `learnware` package we provide. For example, the following code will automatically build the corresponding `conda` environment for the learnware, allowing the learnware to work properly on your device.

```python
from learnware.client import LearnwareClient

# Automatically build a conda environment to load the learnware
client = LearnwareClient()
learnware = client.load_learnware(
    learnware_path=learnware_zip_path, runnable_option="conda"
)

# Use the learnware to make predictions on data
pred_y = learnware.predict(test_x)
```

<!--

## Demo Videos

The following videos provide a more comprehensive demonstration of how to use the Beiming Wu system to solve a machine learning task:

<div style="padding: 56.25% 0 0 0; position: relative"><div style="height:100%;left:0;position:absolute;top:0;width:100%"><iframe height="100%" width="100%;" src="https://embed.wave.video/S2zG1ZbUaRpEo8UG" frameborder="0" allow="autoplay; fullscreen" scrolling="no"></iframe></div></div>

For more information, you can refer to the "[Learnware Search](https://docs.beiming.cloud/en/user-guide/learnware-search.html)" and "[Learnware Deployment](https://docs.beiming.cloud/en/user-guide/learnware-deploy.html)" sections.

If you're interested in sharing your model with the Beiming Wu system, you can quickly get started with the following video:

<div style="padding: 56.25% 0 0 0; position: relative"><div style="height:100%;left:0;position:absolute;top:0;width:100%"><iframe height="100%" width="100%;" src="https://embed.wave.video/JcMSmDcgTJep5zPo" frameborder="0" allow="autoplay; fullscreen" scrolling="no"></iframe></div></div>

For more details, please refer to the "[Learnware Preparation](https://docs.beiming.cloud/en/user-guide/learnware-upload/prepare.html)," "[Uploading via Web Interface](https://docs.beiming.cloud/en/user-guide/learnware-upload/upload-web.html)," and "[Uploading via Client Interface](https://docs.beiming.cloud/en/user-guide/learnware-upload/upload-client.html)" sections.

-->