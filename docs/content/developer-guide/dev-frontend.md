# Beiming System Frontend Development Guide

## Technology Stack

The project is developed using Vue3 + TypeScript + Vite + Vuetify and utilizes pnpm-workspace for managing multiple packages.

- Build Tool: [Vite](https://vitejs.dev/)
- Frontend Framework: [Vue3](https://v3.vuejs.org/)
- UI Framework: [Vuetify](https://vuetifyjs.com/)
- Routing: [Vue Router](https://next.router.vuejs.org/)
- State Management: [Vuex](https://next.vuex.vuejs.org/)

## Directory Structure

The project's directory structure is as follows:

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

It includes the following packages:

- `admin`: Admin system
- `main`: Main system
- `hooks`: Custom hooks
- `locale`: Internationalization
- `types`: Type definitions

## Setting Up the Environment

Install the necessary dependencies:

```bash
cd frontend
npm i -g pnpm
pnpm i
```

## Develop the Main System

```bash
pnpm dev:main
```

## Develop the Admin System

```bash
pnpm dev:admin
```

## Build

```bash
pnpm build
```