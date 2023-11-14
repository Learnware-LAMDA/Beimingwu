# 北冥坞系统前端开发指南

## 技术栈

项目基于 Vue3 + TypeScript + Vite + Vuetify 开发，使用 pnpm-workspace 多包管理。

- 构建工具：[Vite](https://vitejs.dev/)
- 前端框架：[Vue3](https://v3.vuejs.org/)
- UI框架：[Vuetify](https://vuetifyjs.com/)
- 路由：[Vue Router](https://next.router.vuejs.org/)
- 状态管理：[Vuex](https://next.vuex.vuejs.org/)

## 目录结构

项目的目录结构如下：

<details open>
  <summary>/</summary>
  <ul>
    <li>.eslintignore</li>
    <li>.eslintrc.cjs</li>
    <li>.prettierignore</li>
    <li>.prettierrc</li>
    <li>README.md</li>
    <li>package.json</li>
    <li>
      <details>
        <summary>packages</summary>
        <ul>
          <li>
            <details>
              <summary>admin</summary>
              <ul>
                <li>.env</li>
                <li>README.md</li>
                <li>index.html</li>
                <li>package.json</li>
                <li>public</li>
                <li>src</li>
                <li>tsconfig.json</li>
                <li>vite.config.ts</li>
                <li>windi.config.ts</li>
              </ul>
            </details>
          </li>
          <li>
            <details>
              <summary>hooks</summary>
              <ul>
                <li>package.json</li>
                <li>src</li>
                <li>tsconfig.json</li>
                <li>tsup.config.ts</li>
              </ul>
            </details>
          </li>
          <li>
            <details>
              <summary>locale</summary>
              <ul>
                <li>package.json</li>
                <li>src</li>
                <li>tsconfig.json</li>
                <li>tsup.config.ts</li>
              </ul>
            </details>
          </li>
          <li>
            <details>
              <summary>main</summary>
              <ul>
                <li>.env</li>
                <li>index.html</li>
                <li>package.json</li>
                <li>public</li>
                <li>src</li>
                <li>tsconfig.json</li>
                <li>vite.config.ts</li>
                <li>windi.config.ts</li>
              </ul>
            </details>
          </li>
          <li>
            <details>
              <summary>types</summary>
              <ul>
                <li>index.d.ts</li>
                <li>package.json</li>
                <li>src</li>
                <li>tsconfig.json</li>
                <li>tsup.config.ts</li>
              </ul>
            </details>
          </li>
        </ul>
      </details>
    </li>
    <li>pnpm-lock.yaml</li>
    <li>pnpm-workspace.yaml</li>
    <li>shim-vue.d.ts</li>
    <li>tsconfig.eslint.json</li>
    <li>tsconfig.json</li>
    <li>tsup.config.ts</li>
  </ul>
</details>

其中有以下几个包：

- `admin`：管理员系统
- `main`：主系统
- `hooks`：自定义 hooks
- `locale`：国际化
- `types`：类型定义

## 配置环境

安装必要的依赖

```bash
cd frontend
npm i -g pnpm
pnpm i
```

## 开发主系统

```bash
pnpm dev:main
```

## 开发管理员系统

```bash
pnpm dev:admin
```

## 构建

```bash
pnpm build
```
