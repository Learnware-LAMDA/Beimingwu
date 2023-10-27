# 环境安装

为了使用户能够轻松、高效地与北冥系统交互，我们在 `learnware` Python 包中提供了一系列简单且易用的接口。仅需几行代码，大家就能实现「学件规约生成」、「学件上传」、「学件查搜」以及「学件部署」等功能。

`learnware` 包目前托管在 [PyPI 平台](https://pypi.org/project/learnware/)，其具体安装方式如下：
- Windows 和 Linux 系统：
```bash
pip install learnware
```
- macOS 系统：
```bash
conda install -c pytorch faiss
pip install learnware
```

`learnware` 包的源代码同时发布在 [Gitee](https://gitee.com/Learnware-LAMDA/Learnware) 和 [Github](https://github.com/Learnware-LAMDA/Learnware) 平台上，用户也可以从任一平台下载源代码进行安装。以 Github 平台为例：
```bash
git clone https://github.com/Learnware-LAMDA/Learnware.git
cd Learnware
git fetch origin main
git checkout main
pip install -e .
```

请注意，若 Python 版本在 3.11 及以上，可能会有部分依赖无法安装，并对某些功能产生影响。