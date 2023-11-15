# 项目结构与开发规范
## 项目结构
整个项目分为后端，前端，部署和文档4个子项目，具体结构如下所示：
```shell
├── README.md # 项目说明文档
├── backend # 后端目录
│   ├── README.md # 后端说明文档
│   ├── config.py # 后端配置
│   ├── context.py # 后端全局变量
│   ├── database # 数据库目录
│   │   ├── __init__.py
│   │   ├── base.py  # 数据库基类
│   │   └── sqlalchemy.py # 基于sqlalchemy的数据库实现
│   ├── lib # 各类工具
│   │   ├── command_executor.py # 命令行相关
│   │   ├── common_utils.py # 通用
│   │   ├── data_utils.py # 数据相关
│   │   ├── database_operations.py #数据库相关操作
│   │   ├── engine.py # 学件引擎相关工具
│   │   └── redis_utils.py # redis相关
│   ├── requirements.txt # 
│   ├── restful # web接口
│   │   ├── admin.py # 管理员相关接口
│   │   ├── auth.py # 用户认证
│   │   ├── common_functions.py # 通用函数
│   │   ├── engine.py # 引擎接口
│   │   ├── user.py # 用户操作接口
│   │   └── utils.py # 工具函数，如发邮件等
│   ├── scripts # 各类脚本
│   │   ├── backup_data.py # 备份数据
│   │   ├── main.py # web入口
│   │   └── monitor_learnware_verify.py # 学件检查脚本
│   ├── tests # 测试相关代码
│   │   ├── common_test_operations.py # 通用测试函数
│   │   ├── data  # 测试相关数据
│   │   ├── stress_test # 压力测试
│   │   ├── test_admin.py # 管理员接口测试
│   │   ├── test_auth.py # 用户认证测试
│   │   ├── test_backup_data.py # 备份数据测试
│   │   ├── test_command_executor.py # 测试命令执行
│   │   ├── test_engine.py # 测试引擎接口
│   │   ├── test_learnware_client.py # 测试学件客户端
│   │   ├── test_monitor_learnware_verify.py # 测试学件检查脚本
│   │   ├── test_user.py # 测试用户相关接口
│   │   └── test_verify_learnware.py # 测试单个学件检查
├── deploy # 部署相关
│   ├── docker-compose # docker部署相关文件
│   │   └── docker-compose.yaml
│   ├── hooks # git commit检查
│   │   ├── commit-msg # commit message检查
│   │   └── pre-commit # 代码检查
│   ├── kubernetes # kubernetes部署相关
│   │   ├── admin-frontend.yaml # 管理端相关配置
│   │   ├── backend.yaml # 后端部署相关配置
│   │   └── frontend.yaml # 前端部署相关配置
│   └── static # 静态文件
│       └── learnware-template # 学件模版
├── docs # 文档服务相关
│   ├── README.md # 文档服务说明
│   ├── content 
│   │   ├── developer-guide # 开发者指南
│   │   ├── en # 英文文档
│   │   ├── public # 图片
│   │   ├── tsconfig.json # 项目配置
│   │   └── zh-CN # 中文文档
└── frontend # 前端
    ├── README.md # 前端说明
    ├── package.json
    ├── packages 
    │   ├── admin # 管理端模块
    │   │   ├── README.md
    │   │   ├── index.html
    │   │   ├── package.json
    │   │   ├── postcss.config.js
    │   │   ├── public # 图片
    │   │   ├── src # 代码
    │   ├── hooks # commit 检查
    │   ├── locale # 语言切换相关
    │   │   ├── package.json
    │   │   ├── src
    │   │   │   ├── en # 英文文字
    │   │   │   ├── index.ts
    │   │   │   └── zh-cn # 中文文字
    │   │   ├── tsconfig.json
    │   │   └── tsup.config.ts
    │   ├── main # 前端模块
    │   │   ├── index.html
    │   │   ├── package.json
    │   │   ├── postcss.config.js
    │   │   ├── public # 图片
    │   │   ├── src # 代码
    │   │   └── vite.config.ts # 项目配置
    │   └── types # 前端通用类型
```

## 开发规范
### 后端开发规范
#### web接口规范
web接口统一采用flask-restx框架进行开发，每个接口需定义parser，这样可以自动生成swagger说明。

url接口统一放在文件末尾使用add_resource进行添加。

接口默认返回json字符串。返回的http code为200，json字符串须包含code与msg关键字。code为业务代码，一般0代表成功，msg为消息。如果还有额外信息可以放入data字段。

#### 数据库规范
数据库采用SQLAlchemy库进行开发。数据库表定义采用sqlalchemy.ext.declarative进行定义。存取数据采用raw sql进行处理。sql语句必须同时符合sqlite和postgres标准。

#### 异常处理规范
后端捕捉的异常需用logger.exception方法进行输出。

对于业务异常，需要进行捕捉，并在返回json中设置对应的code与msg。对于系统异常，统一返回http code 500。

#### 测试规范
对于每一个web接口需要有对应的单元测试用例。在测试用例中启动模拟后端进行模拟调用然后检查返回值。

通用的测试逻辑（比如清空数据库，注册一个用户等）放在common_test_operations.py里面。

