# Learnware Backend

## 1. 项目结构

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

## 2. Status Code

| Code | Description |
| ---- | ---- |
|   0  | 成功     |
|  1x  | 权限相关错误     |
|  2x  | 请求相关错误    |
|  3x  | 后端相关错误     |
|  4x  | 算法引擎相关错误     |
|  5x  | 具体操作相关错误     |