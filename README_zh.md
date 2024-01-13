<div align=center>
  <img src="./frontend/packages/main/public/logo.svg" width="420" height="auto" style="max-width: 100%;"/>
  <br/>
  <br/>
</div>

<p align="center">
    <a href="https://github.com/Learnware-LAMDA/Beimingwu/blob/main/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/Learnware-LAMDA/Beimingwu?color=blue">
    </a>
    <a href="https://bmwu.cloud/">
        <img alt="Website" src="https://img.shields.io/website/http/docs.bmwu.cloud?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Learnware-LAMDA/Beimingwu/issues">
        <img alt="Open issues" src="https://isitmaintained.com/badge/open/Learnware-LAMDA/Beimingwu.svg">
    </a>
    <a href="https://GitHub.com/Learnware-LAMDA/Beimingwu/pull/">
        <img alt="GitHub pull-requests" src="https://img.shields.io/github/issues-pr/Learnware-LAMDA/Beimingwu.svg">
    </a>
    <a href="https://GitHub.com/Learnware-LAMDA/Beimingwu/commit/">
        <img alt="GitHub latest commit" src="https://badgen.net/github/last-commit/Learnware-LAMDA/Beimingwu">
    </a>
    <a href="https://docs.bmwu.cloud/">
        <img alt="Docs Status" src="https://img.shields.io/website/http/docs.bmwu.cloud?down_color=red&down_message=failing&up_message=success&label=docs">
    </a>
</p>

<h3 align="center">
    <p>北冥坞：学件基座系统</p>
    <p>学件范式的首次系统级实现</p>
    <p>
        <a href="https://github.com/Learnware-LAMDA/Beimingwu/blob/main/README.md">English</a> |
        <b>中文</b>
    </p>
</h3>

# 简介

学件范式由周志华教授在2016年提出 [1, 2]，旨在构建一个巨大的模型平台系统：即学件基座系统，系统地组织管理世界各地的机器学习开发者分享的模型，并通过统一的方式识别、利用已有模型的能力快速解决新的机器学习任务。

北冥坞基于学件范式，首次系统性地实现了学件从上传到部署的完整流程，帮助用户有效查搜和复用学件，而无需从零开始构建机器学习模型。学件由性能优良的机器学习模型和描述模型的规约构成。规约由两部分构成：语义规约通过文本描述模型的功能，而统计规约刻画模型所蕴含的统计信息。

[1] Zhi-Hua Zhou. Learnware: on the future of machine learning. Frontiers of Computer Science, 2016, 10(4): 589–590 <br/>
[2] 周志华. 机器学习: 发展与未来. 中国计算机学会通讯, 2017, vol.13, no.1 (2016 中国计算机大会 keynote)

## 北冥坞系统有哪些特性？

如下图所示，北冥坞首次系统性地实现了学件范式中的核心流程：

- **提交阶段**：系统内置了多重检测机制，以确保上传学件的质量。另外，系统会根据已有的学件规约，训练一个异构引擎，用于合并不同的规约岛屿，以及为学件赋予新规约。随着更多学件的上传，异构引擎将持续更新，实现学件规约的持续迭代，构建更精准的规约世界。
- **部署阶段**：用户上传任务需求后，系统会自动选择是推荐单学件还是多学件组合，并提供高效的部署方式。无论是单个学件还是多学件组合，系统均提供了便捷的学件复用接口。

<div align=center>
  <img src="docs/content/public/overview/learnware-workflow-zh-CN.svg" width="700" height="auto" style="max-width: 100%;"/>
</div>

此外，北冥坞系统还具备以下特性：

- **学件规约生成**：北冥坞系统在 `learnware` Python 包中提供规约生成接口，支持多种数据类型（表格、图像和文本），可以在本地高效生成。
- **学件质量检测**：北冥坞系统内置了多重检测机制，以确保系统中每个学件的质量。
- **学件多样查搜**：北冥坞系统同时支持语义规约和统计规约的查搜，覆盖的数据类型包括表格、图像、文本。另外，对于表格型任务，系统额外支持异构表格学件的查搜。
- **学件本地部署**：北冥坞系统在 `learnware` Python 包中同时提供学件部署与学件复用的接口，帮助用户便捷、安全的部署与复用学件。
- **数据隐私保护**：北冥坞系统所涉及的学件上传、查搜、部署均无需用户上传本地数据，所有涉及的统计规约均由用户本地生成，确保用户数据隐私。
- **面向社区开源**：北冥坞系统面向社区开源，包括 `learnware` Python 包与前后端代码。其中 `leanrware` 包高度可扩展，未来新的规约设计、学件系统设计、学件复用方法都能轻松集成进来。

## 北冥坞系统是如何组织的？

### 系统架构

如下图所示，北冥坞的系统架构包含四个层次，从学件存储层至用户交互层，首次自底向上系统性地实现了学件范式。

四个层次的具体功能如下：

- `学件存储层`：管理以 zip 包格式存储的学件，并通过学件数据库提供相关信息的获取方式；
- `系统引擎层`：囊括了学件范式中的所有流程，包括学件上传、查搜、部署和复用，并独立于后端和前端运行，为学件相关任务和科研探索提供了丰富的算法接口；
- `系统后端层`：实现了北冥坞的工业级部署，提供了稳定的系统在线服务，并通过提供丰富的后端 API 支撑了前端和客户端的用户交互；
- `用户交互层`：实现了基于网页的前端和基于命令行的客户端，为用户交互提供了丰富且便捷的方式。

<div align=center>
  <img src="docs/content/public/overview/beimingwu-architecture-en.svg" width="700" height="auto" style="max-width: 100%;"/>
</div>

### 项目结构

基于上述系统架构，北冥坞项目一共包含如下五个子项目：
- [`系统引擎`](https://github.com/Learnware-LAMDA/Learnware)：实现了学件范式中的核心组件和算法，并提供了一个基于命令行的客户端以便于用户交互，同时将其作为 [learnware](https://pypi.org/project/learnware/) 包发布。
- [`系统前端`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/frontend)：提供了用户与系统交互的界面和功能，包括主系统和管理员系统。
- [`系统后端`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/backend)：负责处理系统的运行逻辑和数据操作，确保系统的稳定性和高性能。
- [`系统文档`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/docs)：维护系统的文档，包括用户指南、开发指南等，确保系统的易用性。
- [`系统部署`](https://github.com/Learnware-LAMDA/Beimingwu/tree/main/deploy)：负责管理系统的部署配置，包括前后端的部署文件。

# 快速上手

欢迎体验[北冥坞系统](https://bmwu.cloud/)！下述内容将帮你快速探索系统网站上的学件查搜功能，并基于 [learnware](https://github.com/Learnware-LAMDA/Learnware) 包提供两个从学件查搜至学件部署的应用案例。

learnware 包的安装可参考：[环境安装](docs/content/zh-CN/overview/installation.md)。

## 学件查搜

在北冥坞系统中，既可以通过语义信息查搜学件，也可以通过统计信息查搜学件。

通过语义信息查搜时，你可以填写目标学件的信息，系统将在学件的名称和描述字段中进行查搜；你也可以通过标签进行筛选。

![image](docs/content/public/quick-start/semantic-search-zh-CN.jpg)

通过统计信息进行查搜时，你需要提交任务的统计信息。我们提供的工具将在保护数据隐私的情况下在本地为你生成任务的近似统计信息。通过下列代码，你可以轻松生成任务的近似统计信息。

```python
from learnware.specification import generate_stat_spec

data_type = "table"  # 数据类型范围: ["table", "image", "text"]
spec = generate_stat_spec(type=data_type, X=test_x)
spec.save("stat.json")
```

通过上传统计信息的 JSON 文件，系统会匹配统计信息接近的学件。你可以通过学件卡片左下角的下载按钮进行学件 zip 包的下载。

![image](docs/content/public/quick-start/stat-search-single-zh-CN.jpg)

某些情况下，多个学件组合在一起的统计信息会更加接近你的任务，系统会将这些学件打包推荐给你。你可以通过右上角的 “下载全部” 按钮进行一键下载。

![image](docs/content/public/quick-start/stat-search-multiple-zh-CN.jpg)

## 示例

北冥坞提供了从学件搜索到学件部署的完整工作流程。以下是两个具体示例。

请注意，下述示例的执行，需要先在北冥坞系统中[注册](https://bmwu.cloud/register)，并获取用户邮箱和客户端令牌。

### 单学件示例

下述代码示例展示了使用北冥坞查搜单个学件，用于预测经典机器学习数据集 Iris 的完整流程。该流程包括统计规约生成、单学件查搜、学件部署，以及最终预测准确率的计算。

```python
from learnware.market import BaseUserInfo
from learnware.specification import generate_stat_spec
from learnware.client import LearnwareClient
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score

# 用户准备
client = LearnwareClient()
client.login(your_email, your_token)
data, target = load_iris(return_X_y=True)
# 生成统计规约
rkme = generate_stat_spec(type="table", X=data)
user_info = BaseUserInfo(stat_info={rkme.type: rkme})

# 查搜单个学件
learnware_id = client.search_learnware(user_info)["single"]["learnware_ids"][0]
print(f"Search result: {learnware_id}")

# 加载学件
learnware = client.load_learnware(learnware_id=learnware_id, runnable_option="conda")

# 复用学件
y_pred = learnware.predict(data)
print(f"Classification accuracy: {accuracy_score(target, y_pred)}")
```

### 多学件示例

下述代码示例展示了使用北冥坞查搜多个学件，用于预测经典机器学习数据集 Digits 的完整流程。该流程包括统计规约生成、多学件查搜、学件部署，以及最终预测准确率的计算。

```python
from learnware.market import BaseUserInfo
from learnware.specification import generate_stat_spec
from learnware.client import LearnwareClient
from learnware.reuse import AveragingReuser
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score

# 用户准备
client = LearnwareClient()
client.login(your_email, your_token)
data, target = load_digits(return_X_y=True)
# 生成统计规约
rkme = generate_stat_spec(type="table", X=data)
user_info = BaseUserInfo(stat_info={rkme.type: rkme})

# 查搜多个学件
learnware_ids = client.search_learnware(user_info)["multiple"]["learnware_ids"]
print(f"Search result: {learnware_ids}")

# 加载学件
learnware_list = client.load_learnware(learnware_id=learnware_ids, runnable_option="conda")

# 复用学件
y_pred = AveragingReuser(learnware_list, mode="vote_by_label").predict(data)
print(f"Classification accuracy: {accuracy_score(target, y_pred)}")
```

# Citation

如果你在研究或工作中使用了我们的项目，请引用下述论文，感谢你的支持！

```bibtex
@article{zhou2022learnware,
  author = {Zhou, Zhi-Hua and Tan, Zhi-Hao},
  title = {Learnware: Small Models Do Big},
  journal = {SCIENCE CHINA Information Sciences},
  year = {2024},
  volume = {67},
  number = {1},
  pages = {1--12},
}
```

# 关于

## 如何贡献

北冥坞系统还很年轻，可能存在错误和问题。我们非常欢迎大家为北冥坞系统做出贡献。
我们为所有的开发者提供了详细的[系统开发指南](https://docs.bmwu.cloud/zh-CN/developer-guide/structure-and-guidelines.html)，并制定了相应的[系统开发规范](https://docs.bmwu.cloud/zh-CN/developer-guide/structure-and-guidelines.html#development-standards)，请大家遵守。
非常感谢大家的贡献！

## 关于我们

北冥坞仓库由 LAMDA 北冥坞研发团队开发和维护，更多信息可参考：[团队简介](https://docs.bmwu.cloud/zh-CN/about-us.html)。