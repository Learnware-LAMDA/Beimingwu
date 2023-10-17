---
outline: deep
---

# 运行时 API 示例

本页演示了由 VitePress 提供的一些运行时 API 的用法。

主要的 `useData()` API 可用于访问当前页面的站点、主题和页面数据。它可以在 `.md` 和 `.vue` 文件中使用：

```md
<script setup>
import { useData } from 'vitepress'

const { theme, page, frontmatter } = useData()
</script>

## 结果

### 主题数据

<pre>{{ theme }}</pre>

### 页面数据

<pre>{{ page }}</pre>

### 页面前言

<pre>{{ frontmatter }}</pre>
```

```vue
<script setup>
import { useData } from "vitepress";

const { site, theme, page, frontmatter } = useData();
</script>

## 结果 ### 主题数据
<pre>{{ theme }}</pre>

### 页面数据
<pre>{{ page }}</pre>

### 页面前言
<pre>{{ frontmatter }}</pre>
```

## 更多

查看[运行时 API 的完整列表文档](https://vitepress.dev/reference/runtime-api#usedata)。

## 方程

$$
\begin{aligned}
\frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2} &= 0, \quad x \in (0, 1), t > 0, \\
u(x, 0) &= \sin(\pi x), \\
u(0, t) &= u(1, t) = 0.
\end{aligned}
$$
