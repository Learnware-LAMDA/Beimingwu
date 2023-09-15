# BM-System
BM System: A realization of learnware paradigm based on RKME specification

## 1 提交规范

commit格式: `<type>`(`<scope>`): `<subject>`
- `<type>` 必须填，有以下几种选择:
    - feat: 新增 feature
    - fix: 修复 bug
    - docs: 修改了文档，比如README、CHANGELOG等
    - style: 修改了格式，包括注释、代码格式、逗号等，不影响代码运行
    - refactor: 代码重构，没有加新功能或修复 bug
    - perf: 优化相关，比如提升性能、体验
    - test: 测试用例，包括单元测试、集成测试等
    - chore: 改变构建流程、或者增加依赖库、工具等
    - revert: 回滚到上一个版本
- `<scope>` 强制为: frontend, backend, deploy; 涉及多个则为 *
- `<subject>` 必须填, 均为英文小写字母

举例, 以下都合法:
- feat(backend): add the modify learnware api
- fix(frontend): modify email verification
- docs(*): add commit rules