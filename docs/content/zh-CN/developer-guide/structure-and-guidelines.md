# 项目结构与开发规范

北冥坞学件基座系统一共包含如下五个子项目：
- **系统引擎**：实现了学件范式中的核心组件和算法，并提供了一个基于命令行的客户端以便于用户交互，同时将其作为 `learnware` 包发布。
- **系统前端**：提供了用户与系统交互的界面和功能，包括主系统和管理员系统。
- **系统后端**：负责处理系统的运行逻辑和数据操作，确保系统的稳定性和高性能。
- **系统文档**：维护系统的文档，包括用户指南、开发指南等，确保系统的易用性。
- **系统部署**：负责管理系统的部署配置，包括前后端的部署文件。

其中「系统引擎」实现于独立的 `Learnware` [代码仓库](https://github.com/Learnware-LAMDA/Learnware)中，并配置了独立的[项目文档](https://learnware.readthedocs.io/en/latest/)。

其余四个子项目则实现于 `Beimingwu` [代码仓库](https://github.com/Learnware-LAMDA/Beimingwu)中，并采用 `Monorepo` 的方式进行管理。下文将介绍 `Beimingwu` 代码仓库的具体结构与开发规范。

## Beimingwu 项目结构

`Beimingwu` 代码仓库包含前端、后端、系统部署、系统文档四个子项目，项目间各自独立。

### 前端项目结构
```shell
├── frontend # 前端项目
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


### 后端项目结构

```shell
├── backend # 后端项目
    ├── README.md # 后端说明文档
    ├── config.py # 后端配置
    ├── context.py # 后端全局变量
    ├── database # 数据库目录
    │   ├── __init__.py
    │   ├── base.py  # 数据库基类
    │   └── sqlalchemy.py # 基于sqlalchemy的数据库实现
    ├── lib # 各类工具
    │   ├── command_executor.py # 命令行相关
    │   ├── common_utils.py # 通用
    │   ├── data_utils.py # 数据相关
    │   ├── database_operations.py #数据库相关操作
    │   ├── engine.py # 学件引擎相关工具
    │   └── redis_utils.py # redis相关
    ├── requirements.txt # 
    ├── restful # web接口
    │   ├── admin.py # 管理员相关接口
    │   ├── auth.py # 用户认证
    │   ├── common_functions.py # 通用函数
    │   ├── engine.py # 引擎接口
    │   ├── user.py # 用户操作接口
    │   └── utils.py # 工具函数，如发邮件等
    ├── scripts # 各类脚本
    │   ├── backup_data.py # 备份数据
    │   ├── main.py # web入口
    │   └── monitor_learnware_verify.py # 学件检查脚本
    ├── tests # 测试相关代码
        ├── common_test_operations.py # 通用测试函数
        ├── data  # 测试相关数据
        ├── stress_test # 压力测试
        ├── test_admin.py # 管理员接口测试
        ├── test_auth.py # 用户认证测试
        ├── test_backup_data.py # 备份数据测试
        ├── test_command_executor.py # 测试命令执行
        ├── test_engine.py # 测试引擎接口
        ├── test_learnware_client.py # 测试学件客户端
        ├── test_monitor_learnware_verify.py # 测试学件检查脚本
        ├── test_user.py # 测试用户相关接口
        └── test_verify_learnware.py # 测试单个学件检查
```

### 系统部署项目结构

```shell
├── deploy # 系统部署项目
    ├── docker-compose # docker部署相关文件
    │   └── docker-compose.yaml
    ├── hooks # git commit检查
    │   ├── commit-msg # commit message检查
    │   └── pre-commit # 代码检查
    ├── kubernetes # kubernetes部署相关
    │   ├── admin-frontend.yaml # 管理端相关配置
    │   ├── backend.yaml # 后端部署相关配置
    │   └── frontend.yaml # 前端部署相关配置
    └── static # 静态文件
        └── learnware-template # 学件模版
```

### 系统文档项目结构

```shell
├── docs # 系统文档项目
    ├── README.md # 文档服务说明
    ├── content 
    │   ├── public # 图片
    │   ├── en # 英文文档
    │   ├── zh-CN # 中文文档
    │   └── tsconfig.json # 项目配置
```

## Beimingwu 开发规范

由于我们采用了 `Monorepo` 的代码管理方式，因此规范 `commit` 格式与项目开发规范非常重要。下文将主要介绍 `hooks` 配置、代码提交规范以及前后端开发规范。

### `hooks` 配置

项目配置了 `hooks`, 具体如下:
- `commit-msg`: 限制 commit 格式；
- `pre-commit`: 在 commit 前自动进行代码格式化。

为使 `hooks` 生效, 需在项目根目录执行下述命令:
```shell
git config core.hooksPath deploy/hooks
```
若为 Linux 系统, 则需要额外赋予相关权限:
```shell
chmod +x deploy/hooks/*
```

### 代码提交规范

北冥坞项目的 `commit` 格式为: `<type>`(`<scope>`): `<subject>`
- `<type>` 必须为下述选项之一:
    - feat: 新增 feature
    - fix: 修复 bug
    - docs: 修改了文档，比如README、CHANGELOG等
    - style: 修改了格式，包括注释、代码格式、逗号等，不影响代码运行
    - refactor: 代码重构，没有加新功能或修复 bug
    - perf: 优化相关，比如提升性能、体验
    - test: 测试用例，包括单元测试、集成测试等
    - chore: 改变构建流程、或者增加依赖库、工具等
    - revert: 回滚到上一个版本
- `<scope>` 有以下几个选项: frontend, backend, docs, deploy
    - 如果涉及多个范围, 则使用逗号连接, 或者直接填写 *
- `<subject>` 必须填, 均为英文小写字母

举例, 以下都合法:
```shell
feat(backend): add the modify learnware api
fix(frontend,backend): fix email verification
docs(*): update README
```

### 后端开发规范

开发后端子项目时，需要遵循一定的规范，主要涉及 web 接口、数据库、异常处理以及测试。

#### web 接口规范

web 接口统一采用 `flask-restx` 框架进行开发，每个接口需定义 `parser`，这样可以自动生成 `swagger` 说明。

url 接口统一放在文件末尾使用 `add_resource` 进行添加。

接口默认返回 `json` 字符串。返回的 `http code` 为 200，`json` 字符串须包含 `code` 与 `msg` 关键字。`code` 为业务代码，一般 0 代表成功，`msg` 为消息。如果还有额外信息可以放入 `data` 字段。

#### 数据库规范

数据库采用 `SQLAlchemy` 库进行开发。数据库表定义采用 `sqlalchemy.ext.declarative` 进行定义。存取数据采用 `raw sql` 进行处理。`sql` 语句必须同时符合 `sqlite` 和 `postgres` 标准。

#### 异常处理规范

后端捕捉的异常需用 `logger.exception` 方法进行输出。

对于业务异常，需要进行捕捉，并在返回的 `json` 中设置对应的 `code` 与 `msg`。对于系统异常，统一返回 `http code 500`。

#### 测试规范

对于每一个 web 接口需要有对应的单元测试用例。在测试用例中启动模拟后端进行模拟调用然后检查返回值。

通用的测试逻辑（比如清空数据库，注册一个用户等）放在 `common_test_operations.py` 里面。

