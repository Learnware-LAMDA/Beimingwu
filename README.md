# Learnware Market 规范

## 1 提交规范

### 1.1 Commit 内容

请按照以下方式提交：
按照 前缀 + Space + 后缀 的方法提交
* 前缀有三种选择，可使用逗号链接
  *  [ENH]：表示 enhancement，意味着增加新功能
  *  [DOC]：表示修改了文档
  *  [FIX]：表示修改了 bug，修改了 tyoo
  *  [MNT]：表示其他小修改，比如更新版本号

* 后缀表示具体修改的内容，首字母大写
  
* 举例：一下都合法
  * [DOC] Fix the document
  * [FIX, ENT] Fix the bug and add some feature

### 1.2 格式

提交前使用以下命令进行format：
```
black -l 120 .
```
其中black安装命令为：
```
pip install black
```

> Copied from Learnware market