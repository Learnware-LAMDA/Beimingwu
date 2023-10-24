# 如何准备一个学件？

在北冥系统中，每个学件都是一个 `zip` 包，其中至少需要包含以下四个文件：
- `learnware.yaml`：学件配置文件；
- `__init__.py`：提供使用模型的方法；
- `stat.json`：学件的统计规约，其文件名可自定义并记录在 learnware.yaml 中；
- `environment.yaml` 或 `requirements.txt`：指明模型的运行环境。

创建上述四个文件时，需要使用 `learnware` Python 包，其具体安装方式可查看：[环境安装](/zh-CN/overview/installation)。

为方便大家构建学件，我们提供了[学件模板](http://www.lamda.nju.edu.cn/learnware/static/learnware-template.zip)，大家可在其基础上构建自己的学件。

接下来，我们将详细介绍上述四个文件的具体内容。


## 模型调用文件 `__init__.py`


为了使上传的学件可以被后续用户使用，需在 \_\_init\_\_.py 中提供模型拟合 (fit)、预测 (predict)、微调 (fine-tuning) 的接口。三个接口中仅 predict 为必须提供的接口，其余接口根据模型本身功能而定。此处给出 \_\_init\_\_.py 文件的模板格式：
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

需要注意 MyModel 类要继承 learnware.model 中的 BaseModel，且类的名字（e.g., MyModel）需要在后续的 learnware.yaml 文件中标明。

另外，如果 \_\_init\_\_.py 文件中需要导入 zip 包内其它的模块，请采用相对导入的方式。例如：
```py
from .package_name import *
from .package_name import module_name
```

## 学件统计规约 `stat.json`

学件由模型和规约组成，因此在准备好模型后，我们需要为它生成统计规约。具体来说，使用先前安装的 `learnware` 包，将模型的训练数据 `train_x`（支持的类型包括：numpy.ndarray、pandas.DataFrame 以及 torch.Tensor）作为输入，即可生成模型的统计规约。

以下是相应的代码示例：

```py
import learnware.specification as specification

spec = specification.utils.generate_rkme_spec(train_x)
spec.save("stat.json")
```
值得注意的是，上述代码仅在本地计算机上运行，不会与任何云服务器进行交互，也不会泄露任何本地私有数据。

## 学件配置文件 `learnware.yaml`

该文件用于指明模型调用文件 \_\_init\_\_.py 中的类名 (`MyModel`)、生成统计规约所调用的模块 (`learnware.specification`) 以及统计规约的类别 (`RKMEStatSpecification`) 与具体的文件名 (`stat.json`)：
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

需注意，使用上述 `generate_rkme_spec` 方法生成的规约即为 `RKMEStatSpecification`，因此 `class_name` 按默认值填即可。

## 模型运行依赖 `environment.yaml`

为了使上传的学件可以被后续其它用户使用，上传学件的 `zip` 包中需指明模型的运行依赖：
- 此处推荐大家提供 `conda` 支持的 `environment.yaml` 文件，该文件可通过下述命令由 `conda` 虚拟环境直接导出：
    - Linux 和 macOS 系统：
    ```bash
    conda env export | grep -v "^prefix: " > environment.yaml
    ```
    - Windows 系统：
    ```bash
    conda env export | findstr /v "^prefix: " > environment.yaml
    ```
- 除上述方式外，也可以提供 `pip` 支持的 `requirements.txt` 文件。该文件需要列出运行 `__init__.py` 文件所需导入的包及其具体版本，这些版本信息可通过执行 `pip show <package_name>` 或 `conda list <package_name>` 命令来获取。以下是一个示例文件：
    ```txt
    learnware==0.1.0.999
    numpy==1.23.5
    scikit-learn==1.2.2
    ```
    手动列举可能会有些麻烦，也可以使用 `pipreqs` 包直接扫描整个项目，自动导出使用的包及其具体版本（但很可能会有些偏差，需要再自行检查）：
    ```bash
    pip install pipreqs
    pipreqs ./  # 需在项目根目录执行
    ```

无论使用哪一种方式，请尽量去除不需要的依赖，使依赖项尽可能的少。

## 学件本地验证

上述文件填写完毕后，即可进行学件上传。一旦学件成功上传，系统后台会自动将该学件加入验证队列，以检验学件是否符合规范（包括学件格式以及模型是否可运行的检查）。这个验证过程可能需要一些时间，具体取决于学件的复杂程度以及系统后台的工作负载。完成验证后，结果将在网页端显示。

由于后台验证学件的过程相对耗时，为了提高学件通过验证的几率，我们建议您在上传之前，先使用以下代码在本地对学件进行验证：
```py
from learnware.client import LearnwareClient

zip_path = "learnware.zip"  # 待验证的学件 zip 包
LearnwareClient.check_learnware(zip_path)
```

在本地成功通过验证后，再将学件上传至系统，以提高学件验证效率。