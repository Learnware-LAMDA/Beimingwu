# BM-System
BM System: A realization of learnware paradigm based on RKME specification

## 1 hooks 配置

项目配置了 hooks, 具体如下: 
- `commit-msg`: 限制 commit 格式
- `pre-commit`: 在 commit 前自动进行代码格式化

为使 hooks 生效, 需在项目根目录执行下述命令:

```bash
git config core.hooksPath deploy/hooks
```

若为 Linux 系统, 则需要额外赋予相关权限:
```bash
chmod +x deploy/hooks/*
```

## 2 提交规范

commit格式: `<type>`(`<scope>`): `<subject>`
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
- feat(backend): add the modify learnware api
- fix(frontend,backend): fix email verification
- docs(*): update README