# 环境安装

为了使用户能够轻松、高效地与北冥坞系统交互，我们在 `learnware` Python 包中提供了一系列简单且易用的接口。仅需几行代码，大家就能实现「学件规约生成」、「学件上传」、「学件查搜」以及「学件部署」等功能。

## 通过 `pip` 安装

`learnware` 包目前托管在 [PyPI 平台](https://pypi.org/project/learnware/)，其具体安装方式如下：
```bash
pip install learnware
```

此外，为确保安装的 `learnware` 包为最新版本，也可通过指定版本和镜像源的方式进行安装：
```bash
pip install learnware==0.2.0.9 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 通过源码安装

`learnware` 包的源代码发布在 [Gitee](https://gitee.com/beimingwu/beimingwu) 平台上，用户也可以从任一平台下载源代码进行安装。以 Github 平台为例：
```bash
git clone https://gitee.com/beimingwu/beimingwu
cd Learnware
git fetch origin main
git checkout main
pip install -e .
```

## 注意事项

在 `learnware` 包中，除了基础类之外，许多核心功能（如学件规约生成、学件部署等）都需要依赖 `torch` 库。用户可选择手动安装 `torch`，或直接采用以下命令安装 `learnware` 包：
```bash
pip install learnware[full]
```
但需要特别注意的是，由于用户本地环境可能较为复杂，安装 `learnware[full]` 并不能确保 `torch` 能够在用户的本地环境成功调用 `CUDA`。