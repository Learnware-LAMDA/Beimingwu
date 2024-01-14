# Environment Installation

In order to enable users to interact with the Beimingwu system easily and efficiently, we provide a series of simple and user-friendly interfaces in the `learnware` Python package. With just a few lines of code, everyone can implement functions such as "learnware specification generation", "learnware search", and "learnware deployment".

## Install via pip

The `learnware` package is currently avabilable on the [PyPI](https://pypi.org/project/learnware/), and its specific installation method is as follows:
```bash
pip install learnware
```

Additionally, to ensure the latest `learnware` package, you can also specify the version and mirror source during installation:
```bash
pip install learnware==0.2.0.9 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## Install from Source Code

The source code for the `learnware` package is also available on [Gitee](https://gitee.com/beimingwu/beimingwu) platform. Users can download the source code from either platform for installation. Here is an example when using the Github platform:
```bash
git clone https://gitee.com/beimingwu/beimingwu
cd Learnware
git fetch origin main
git checkout main
pip install -e .
```

## Important Notes

In the `learnware` package, besides the base classes, many core functionalities such as "learnware specification generation" and "learnware deployment" rely on the `torch` library. Users have the option to manually install `torch`, or they can directly use the following command to install the `learnware` package:
```bash
pip install learnware[full]
```
However, it's crucial to note that due to the potential complexity of the user's local environment, installing `learnware[full]` does not guarantee that `torch` will successfully invoke CUDA in the user's local setting.