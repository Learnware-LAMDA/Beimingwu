# 如何准备一个学件？

在北冥系统中，每个学件都是一个 `zip` 包，其中至少需要包含以下四个文件：
- `learnware.yaml`：学件配置文件；
- `__init__.py`：提供使用模型的方法；
- `stat.json`：学件的统计规约，其文件名可自定义并记录在 learnware.yaml 中；
- `environment.yaml` 或 `requirements.txt`：指明模型的运行环境。

创建上述四个文件时，需要使用 `learnware` Python 包，其具体安装方式可查看：[环境安装](/zh-CN/overview/installation)。

接下来，我们将详细介绍这四个文件的具体内容。


## 模型调用文件 `__init__.py`



## 学件统计规约 `stat.json`


## 学件配置文件 `learnware.yaml`


## 模型运行依赖 `environment.yaml`