# Beimingwu System Frontend

The project is developed based on Vue3 + TypeScript + Vite + Vuetify, using pnpm-workspace for multi-package management.

- Build Tool: [Vite](https://vitejs.dev/)
- Frontend Framework: [Vue3](https://v3.vuejs.org/)
- UI Framework: [Vuetify](https://vuetifyjs.com/)
- Router: [Vue Router](https://next.router.vuejs.org/)
- State Management: [Vuex](https://next.vuex.vuejs.org/)

It includes the following packages:

- `admin`: Admin system
- `main`: Main system
- `hooks`: Custom hooks
- `locale`: Internationalization
- `types`: Type definitions

## Configuration

Install the necessary dependencies

```bash
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