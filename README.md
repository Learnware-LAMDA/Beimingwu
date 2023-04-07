# Learnware Backend

## 1 提交规范

> Copied from learnware engine group

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



## 2 项目结构

* api: 接口处理逻辑
  * auth.py: 账户接口逻辑
  * user.py: 用户接口逻辑
  * admin.py: 管理员接口逻辑
  * engine.py: 算法引擎接口逻辑
  * utils.py: 接口处理需要的工具函数
* database: 数据库执行（允许兼容多种数据库）
  * base.py: 数据库基类
  * sqlite.py: SQLite 数据库类
* lib: 数据库、算法引擎的交互逻辑
  * sqlite.py: 与 SQLite 数据库交互
  * engine.py: 与算法引擎交互（暂未完成）
* files: 保存临时文件，例如：SQLite 数据库文件
  * database.db
  * uplaod: 缓存文件区
* config.py: 全局配置与变量
* main.py: 主程序
* environment.yaml: 环境配置

## 3. Status Code

| Code | Description |
| ---- | ---- |
|   0  | 成功     |
|  1x  | 权限相关错误     |
|  2x  | 请求相关错误    |
|  3x  | 后端相关错误     |
|  4x  | 算法引擎相关错误     |
|  5x  | 具体操作相关错误     |
