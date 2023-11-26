# 如何准备一个学件？

在北冥坞系统中，每个学件都是一个 `zip` 包，其中至少需要包含以下四个文件：
- `learnware.yaml`：学件配置文件；
- `__init__.py`：提供使用模型的方法；
- `stat.json`：学件的统计规约，其文件名可自定义并记录在 learnware.yaml 中；
- `environment.yaml` 或 `requirements.txt`：指明模型的运行环境。

创建上述四个文件时，需要使用 `learnware` Python 包，其具体安装方式可查看：[环境安装](/zh-CN/overview/installation)。

为方便大家构建学件，我们提供了[学件模板](http://www.bmwu.cloud/static/learnware-template.zip)，大家可在其基础上构建自己的学件。

接下来，我们将详细介绍上述四个文件的具体内容。


## 模型调用文件 `__init__.py`


为了使上传的学件可以被后续用户使用，需在 \_\_init\_\_.py 中提供模型拟合 `fit(X, y)`、预测 `predict(X)`、微调 `finetune(X, y)` 的接口。三个接口中仅 `predict(X)` 为必须提供的接口，其余接口根据模型本身功能而定。

以下是 `__init__.py` 文件的参考模板，请确保您上传的模型调用文件中各个接口输入参数的格式（参数个数、参数名）与下述模板保持一致：
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

需要注意 MyModel 类要继承 `learnware.model` 中的 BaseModel，且类的名字（e.g., MyModel）需要在后续的 learnware.yaml 文件中标明。

### 输入输出维度

`input_shape` 、`output_shape` 分别代表模型的输入和输出维度，填写时可参考下述规范：
- `input_shape` 是单个输入样本的维度，`output_shape` 是模型对于单个样本的输出维度；
- 当学件处理的数据类型为文本数据时，对 `input_shape` 的具体值不作要求，可填写为 `None`；
- 当学件对应任务的 `output_shape` 不固定时（例如目标检测、文本分割等任务），对 `output_shape` 的具体值不作要求，可填写为 `None`；
- 对于分类任务，如果模型直接输出预测标记，则 `output_shape` 应填写为 (1, )；若模型输出为类别的后验概率，则 `output_shape` 应填写为类别数目，即 (class_num, ) 的形式。

### 文件路径

如果在 `__init__.py` 文件（以及其它可能涉及的 Python 文件）中需要导入 zip 包内某些文件时（例如模型文件 `model.pkl`），请采用上述示例代码中获取 `model_path` 的方式：
- 先获取整个学件包的根目录路径 `dir_path`；
- 再根据具体文件在包内的相对位置，获取具体文件的路径 `model_path`。

### 模块引用

请注意，zip 包内 Python 文件之间的模块引用应采用**相对引用**的方式。例如：
```py
from .package_name import *
from .package_name import module_name
```

## 学件统计规约 `stat.json`

学件由模型和规约组成，因此在准备好模型后，我们需要为它生成统计规约。具体来说，使用先前安装的 `learnware` 包，将模型的训练数据 `train_x`（支持的类型包括：numpy.ndarray、pandas.DataFrame 以及 torch.Tensor）作为输入，即可生成模型的统计规约。

以下是相应的代码示例：

```py
from learnware.specification import generate_stat_spec

data_type = "table" # 数据类型范围: ["table", "image", "text"]
spec = generate_stat_spec(type=data_type, X=train_x)
spec.save("stat.json")
```
值得注意的是，上述代码仅在本地计算机上运行，不会与任何云服务器进行交互，也不会泄露任何本地私有数据。

另外，如果由于模型的训练数据过大而导致上述代码执行失败，您可以考虑先对训练数据进行采样，以确保其大小适中，然后再进行规约生成。

## 学件配置文件 `learnware.yaml`

该文件用于指明模型调用文件 \_\_init\_\_.py 中的类名 (`MyModel`)、生成统计规约所调用的模块 (`learnware.specification`) 以及统计规约的类别 (`RKMETableSpecification`) 与具体的文件名 (`stat.json`)：
```yaml
model:
  class_name: MyModel
  kwargs: {}
stat_specifications:
  - module_path: learnware.specification
    class_name: RKMETableSpecification
    file_name: stat.json
    kwargs: {}
```

需注意，生成规约时的数据类型 `["table", "image", "text"]` 所对应的规约类型分别为 `[RKMETableSpecification, RKMEImageSpecification, RKMETextSpecification]`。

## 模型运行依赖

为了使上传的学件可以被后续其它用户使用，上传学件的 `zip` 包中需指明模型的运行依赖。北冥坞系统支持下述两种指定运行依赖的方式：
- 提供 `conda` 支持的 `environment.yaml` 文件；
- 提供 `pip` 支持的 `requirements.txt` 文件。

两种方式选其一即可，但无论使用哪一种方式，请尽量去除不需要的依赖，使依赖项尽可能的少。

### 使用 `environment.yaml` 文件

`environment.yaml` 文件可通过下述命令由 `conda` 虚拟环境直接导出：
- Linux 和 macOS 系统：
```bash
conda env export | grep -v "^prefix: " > environment.yaml
```
- Windows 系统：
```bash
conda env export | findstr /v "^prefix: " > environment.yaml
```

需要注意的是， 学件 `zip` 包中的 `environment.yaml` 文件需要使用 `UTF-8` 格式编码。在导出后，请检查 `environment.yaml` 文件的编码格式。由于 `conda` 版本和系统的差异，您可能会得到非 `UTF-8` 格式编码的文件（例如 `UTF-16LE` 格式），此时需要手动将文件转换为 `UTF-8` 编码格式。大多数文本编辑器都支持编码格式转换。您也可以参考下述编码转换的 `Python` 代码：

```python
import codecs

# 读取 conda env export 命令的输出文件
# 这里假设文件名为 environment.yaml, 导出格式为 UTF-16LE
with codecs.open('environment.yaml', 'r', encoding='utf-16le') as file:
    content = file.read()

# 将内容转换为 UTF-8 编码
output_content = content.encode('utf-8')

# 写入 UTF-8 编码的文件
with open('environment.yaml', 'wb') as file:
    file.write(output_content)
```

另外，由于用户本地 `conda` 虚拟环境的复杂性，您可以在上传前执行以下命令，以确认您上传的 `environment.yaml` 文件中不存在内部依赖冲突：
```bash
conda env create --name test_env --file environment.yaml
```

上述命令将根据 `environment.yaml` 文件创建虚拟环境，若创建成功，则说明文件不存在依赖冲突。创建的虚拟环境可通过下述命令进行删除：
```bash
conda env remove --name test_env
```

### 使用 `requirements.txt` 文件

`requirements.txt` 文件需要列出运行 `__init__.py` 文件所需安装的包以及它们的具体版本。这些版本信息可通过执行 `pip show <package_name>` 或 `conda list <package_name>` 命令来获取。以下是一个示例文件：
```txt
numpy==1.23.5
scikit-learn==1.2.2
```
如果觉得手动列举比较麻烦，也可以使用 `pipreqs` 包直接扫描整个项目，自动导出使用的包及其具体版本（但很可能会有些偏差，需要再自行检查）：
```bash
pip install pipreqs
pipreqs ./  # 需在项目根目录执行
```
请注意，如果您使用 `requirements.txt` 文件来指定运行依赖，系统在学件部署时将默认在 `Python 3.8` 的 `conda` 虚拟环境中安装这些依赖。

此外，对于一些对版本十分敏感的包（例如 `torch`），请务必在 `requirements.txt` 文件中指定包的版本，否则可能会导致上传的学件无法在其它机器上部署。


## 学件本地验证

上述文件填写完毕后，即可进行学件上传。一旦学件成功上传，系统后台会自动将该学件加入验证队列，以检验学件是否符合规范（包括学件格式以及模型是否可运行的检查）。这个验证过程可能需要一些时间，具体取决于学件的复杂程度以及系统后台的工作负载。完成验证后，结果将在网页端显示。

由于后台验证学件的过程相对耗时，为了提高学件通过验证的几率，我们建议您在上传之前，先使用以下代码在本地对学件进行验证：
```py
from learnware.client import LearnwareClient

zip_path = "learnware.zip"  # 待验证的学件 zip 包
LearnwareClient.check_learnware(zip_path)
```

在本地成功通过验证后，再将学件上传至系统，以提高学件验证效率。
