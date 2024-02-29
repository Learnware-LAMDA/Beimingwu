<div align=center>
  <img src="./frontend/packages/main/public/logo.svg" width="420" height="auto" style="max-width: 100%;"/>
  <br/>
  <br/>
</div>

<div align="center">
    <a href="LICENSE">
        <img alt="LICENSE" src="https://img.shields.io/pypi/l/learnware?color=blue">
    </a>
    <a href="https://bmwu.cloud/">
        <img alt="Website" src="https://img.shields.io/website/http/docs.bmwu.cloud?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://pypi.org/project/learnware/#history">
        <img alt="PypI Versions" src="https://img.shields.io/pypi/v/learnware">
    </a>
    <a href="https://pypi.org/project/learnware/#files">
        <img alt="Platform" src="https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey">
    </a>
    <a href="https://docs.bmwu.cloud/">
        <img alt="Docs Status" src="https://img.shields.io/website/http/docs.bmwu.cloud?down_color=red&down_message=failing&up_message=success&label=docs">
    </a>
    <a href="https://img.shields.io/pypi/dm/example-package">
        <img alt="PyPI Downloads" src="https://img.shields.io/pypi/dm/example-package">
    </a>
</div>

<div>
    <h3 align="center">Beimingwu: The First Learnware Dock System</h3>
    <h3 align="center">A Research Platform for Learnware</h3>
    <h3 align="center">
        <a href="README_zh.md">中文</a> |
        <b>English</b>
    </h3>
</div>

# Introduction

_Learnware_ was proposed by Professor Zhi-Hua Zhou in 2016 [1, 2]. In the _learnware paradigm_, developers worldwide can share models with the _learnware dock system_, which effectively searches for and reuse learnware(s) to help users solve machine learning tasks efficiently without starting from scratch.

Beimingwu is the first systematic open-source implementation of learnware dock system, providing a preliminary research platform for learnware studies. Developers worldwide can submit their models freely to the learnware dock. They can generate specifications for the model with the help of Beimingwu without disclosing their raw data, and then the model and specification can be assembled into a learnware, which will be accommodated in the learnware dock. Future users can solve their tasks by submitting their requirements and reusing helpful learnwares returned by Beimingwu, while also not disclosing their own data. It is anticipated that after Beimingwu accumulates millions of learnwares, an "emergent" behavior may occur: machine learning tasks that have never been specifically tackled may be solved by assembling and reusing some existing learnwares.

A learnware is a well-performed trained model with a specification that describes its capabilities, enabling it to be readily identified and reused in the future based on user requirements. The specification includes a semantic specification in text and a statistical specification sketching the model's statistical information.

[1] Zhi-Hua Zhou. Learnware: on the future of machine learning. _Frontiers of Computer Science_, 2016, 10(4): 589–590 <br/>
[2] Zhi-Hua Zhou. Machine Learning: Development and Future. _Communications of CCF_, 2017, vol.13, no.1 (2016 CNCC keynote)

## What features does Beimingwu have?

As shown in the diagram below, the Beimingwu learnware dock system, serving as a preliminary research platform for learnware, systematically implements the core processes of the learnware paradigm for the first time:

- **Submitting Stage**: The system includes multiple detection mechanisms to ensure the quality of uploaded learnwares. Additionally, the system trains a heterogeneous engine based on existing learnware specifications in the system to merge different specification islands and assign new specifications to learnwares. With the submission of more learnwares, the heterogeneous engine will continually update, aiming to construct a more precise specification world through the constant iteration of learnware specifications.
- **Deploying Stage**: After users upload task requirements, the system automatically selects whether to recommend a single learnware or multiple learnware combinations and provides efficient deployment methods. Whether it's a single learnware or a combination of multiple learnwares, the system offers baseline learnware reuse methods in a uniform format for convenient usage.

<div align=center>
  <img src="docs/content/public/overview/learnware-workflow-en.svg" width="700" height="auto" style="max-width: 100%;"/>
</div>

In addition, the Beimingwu system also has the following features:

- **Learnware Specification Generation**: The Beimingwu system provides specification generation interfaces in the `learnware` Python package, supporting various data types (tables, images, and text) for efficient local generation.
- **Learnware Quality Inspection**: The Beimingwu system includes multiple detection mechanisms to ensure the quality of each learnware in the system.
- **Diverse Learnware Search**: The Beimingwu system supports both semantic specifications and statistical specifications searches, covering data types such as tables, images, and text. In addition, for table-based tasks, the system preliminarily supports the search for heterogeneous table learnwares.
- **Local Learnware Deployment**: The Beimingwu system provides a unified user interface for learnware deployment and reuse in the `learnware` Python package, facilitating users' convenient deployment and reuse of arbitrary learnwares.
- **Raw Data Protection**: The Beimingwu system operations, including learnware submission, identification, and deployment, do not require users to upload raw data. All relevant statistical specifications are generated locally by users using open-source API.
- **Open Source System**: The Beimingwu system's source code is open-source, including the `learnware` Python package and frontend/backend code. The `learnware` package is highly extensible, making it easy to integrate new specification designs, learnware system designs, and learnware reuse methods in the future.

## How is Beimingwu organized?

### System Architecture

As depicted in the figure below, Beimingwu's architecture consists of four hierarchical layers, from the learnware storage layer to the user interaction layer, systematically implementing the learnware paradigm for the first time from the ground up.

The functionalities of the four layers are described as follows:
- `Learnware Storage Layer`: Manage the storage of learnwares in zip packages and provides access to them through the learnware database.
- `Core Engine Layer`: Encompass all processes within the learnware paradigm, including learnware uploading, searching, reusing, and deployment, and operate independently of the backend and frontend, offering rich algorithmic interfaces for learnware-related tasks and research experiments.
- `System Backend Layer`: Enable industrial-level deployment of Beimingwu, offering stable online deployment and providing extensive backend APIs for frontend and client interactions.
- `User Interface Layer`: Comprise a web-based frontend and a command-line client for user convenience and interaction.

<div align=center>
  <img src="docs/content/public/overview/beimingwu-architecture-en.svg" width="700" height="auto" style="max-width: 100%;"/>
</div>

### Project Structure

Based on the system architecture, Beimingwu is developed with five sub-projects:
- [`Engine`](https://github.com/Learnware-LAMDA/Learnware): Encompassing core components and algorithms within the learnware paradigm, and providing a command-line client for user interaction, it has been releasead as the [learnware](https://pypi.org/project/learnware/) package.
- [`Frontend`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/frontend): Provide the interface and functionality for user interaction with the learnware dock system, including the main system and administrator system.
- [`Backend`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/backend): Responsible for handling the dock system's operation logic and data operations, it ensures system stability and high performance.
- [`Docs`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/docs): Maintain system documentation, including user guides, development guides, etc., ensuring system usability.
- [`Deploy`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/deploy): Manage the system deployment configuration, including frontend and backend deployment files.

# Quick Start

Welcome to experience [Beimingwu](https://bmwu.cloud/). The following instructions will assist you in quickly exploring the search functionality on the system website and provide two demo cases from learnware search to learnware deployment using the [learnware](https://github.com/Learnware-LAMDA/Learnware) package.

The installation instructions for the learnware package can be found here: [Installation Guide](docs/content/en/overview/installation.md).

## Learnware Search

In Beimingwu, learnwares can be searched using both semantic information and statistical information.

When searching with semantic information, you can fill in the information about your target learnware, and the system will search in the names and descriptions of learnwares. You can also filter by tags.

![image](docs/content/public/quick-start/semantic-search-en.jpg)

When searching with statistical information, you need to generate and submit a statistical specification, which captures the data distribution while not disclosing your original data. Using the API we provided, you can easily generate this statistical specification locally.

```python
from learnware.specification import generate_stat_spec

data_type = "table"  # Data types: ["table", "image", "text"]
spec = generate_stat_spec(type=data_type, X=test_x)
spec.save("stat.json")
```

By uploading the JSON file containing statistical information, the system will match learnware with similar statistical information. You can download the learnware zip by clicking on the download button in the lower left corner of the learnware card.

![image](docs/content/public/quick-start/stat-search-single-en.jpg)

In some cases, assembling multiple helpful learnwares may be more beneficial for your task. The system will accordingly recommend a combination of these learnwares as a package. You can download the package using the "Download All" button in the upper right corner.

![image](docs/content/public/quick-start/stat-search-multiple-en.jpg)

## Demo Cases

Beimingwu offers a complete workflow from learnware search to learnware deployment. Below are two specific examples.

Please note that to execute the following examples, you need to first [register](https://bmwu.cloud/register) in the Beimingwu system and obtain a user email and client token.

### Single Learnware Demo

The following demo illustrates the complete process of using Beimingwu to search for a single learnware for predicting the classic machine learning dataset Iris. This process includes statistical specification generation, single learnware search, learnware deployment, and the final calculation of prediction accuracy.

```python
from learnware.market import BaseUserInfo
from learnware.specification import generate_stat_spec
from learnware.client import LearnwareClient
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# User prepare
client = LearnwareClient()
client.login(your_email, your_token)
data, target = load_iris(return_X_y=True)
# Generate statistical specification
rkme = generate_stat_spec(type="table", X=data)
user_info = BaseUserInfo(stat_info={rkme.type: rkme})

# Search a single learnware
learnware_id = client.search_learnware(user_info)["single"]["learnware_ids"][0]
print(f"Search result: {learnware_id}")

# Load learnware
learnware = client.load_learnware(learnware_id=learnware_id, runnable_option="conda")

# Reuse learnware
y_pred = learnware.predict(data)
print(f"Classification accuracy: {accuracy_score(target, y_pred)}")
```

### Multiple Learnwares Demo

The following demo illustrates the complete process of using Beimingwu to search for multiple learnwares for predicting the classic machine learning dataset Digits. This process includes statistical specification generation, multiple learnware search, learnware deployment, and the final calculation of prediction accuracy.

```python
from learnware.market import BaseUserInfo
from learnware.specification import generate_stat_spec
from learnware.client import LearnwareClient
from learnware.reuse import AveragingReuser
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score

# User prepare
client = LearnwareClient()
client.login(your_email, your_token)
data, target = load_digits(return_X_y=True)
# Generate statistical specification
rkme = generate_stat_spec(type="table", X=data)
user_info = BaseUserInfo(stat_info={rkme.type: rkme})

# Search multiple learnwares
learnware_ids = client.search_learnware(user_info)["multiple"]["learnware_ids"]
print(f"Search result: {learnware_ids}")

# Load learnware
learnware_list = client.load_learnware(learnware_id=learnware_ids, runnable_option="conda")

# Reuse learnware
y_pred = AveragingReuser(learnware_list, mode="vote_by_label").predict(data)
print(f"Classification accuracy: {accuracy_score(target, y_pred)}")
```

# Citation

If you use our project in your research or work, we kindly request that you cite the following papers:

```bibtex
@article{zhou2024learnware,
  title = {Learnware: Small models do big},
  author = {Zhou, Zhi-Hua and Tan, Zhi-Hao},
  journal = {Science China Information Sciences},
  volume = {67},
  number = {1},
  pages = {112102},
  year = {2024}
}

@article{tan2024beimingwu,
  title = {Beimingwu: A learnware dock system}, 
  author = {Tan, Zhi-Hao and Liu, Jian-Dong and Bi, Xiao-Dong and Tan, Peng and Zheng, Qin-Cheng and Liu, Hai-Tian and Xie, Yi and Zou, Xiao-Chuan and Yu, Yang and Zhou, Zhi-Hua},
  journal = {arXiv preprint arXiv:2401.14427},
  year = {2024}
}
```

# About

## How to Contribute

Building the learnware paradigm requires collective efforts from the community. As the first learnware dock system, Beimingwu is still in its early stages and may contain bugs and issues. We sincerely invite the community to upload models, collaborate in system development, and engage in research and enhancements in learnware algorithms. For detailed development guidelines, please consult our [Developer Guide](https://docs.bmwu.cloud/en/developer-guide/structure-and-guidelines.html). We kindly request that contributors adhere to the provided [Development Standards](https://docs.bmwu.cloud/en/developer-guide/structure-and-guidelines.html#development-standards) when participating in the project. Your valuable contributions are greatly appreciated.

## About Us

The Beimingwu repository is developed and maintained by the LAMDA Beimingwu R&D (Research and Development) Team. To learn more about our team, please visit the [Team Overview](https://docs.bmwu.cloud/en/about-us.html).
