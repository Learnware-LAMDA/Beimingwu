---
outline: deep
---

# 運行時 API 範例

本頁演示了由 VitePress 提供的一些運行時 API 的用法。

主要的 `useData()` API 可用於訪問當前頁面的站點、主題和頁面數據。它可以在 `.md` 和 `.vue` 文件中使用：

```md
<script setup>
import { useData } from 'vitepress'

const { theme, page, frontmatter } = useData()
</script>

## 結果

### 主題數據

<pre>{{ theme }}</pre>

### 頁面數據

<pre>{{ page }}</pre>

### 頁面前言

<pre>{{ frontmatter }}</pre>
```

```vue
<script setup>
import { useData } from "vitepress";

const { site, theme, page, frontmatter } = useData();
</script>

## 結果 ### 主題數據
<pre>{{ theme }}</pre>

### 頁面數據
<pre>{{ page }}</pre>

### 頁面前言
<pre>{{ frontmatter }}</pre>
```

## 更多

查看[運行時 API 的完整列表文檔](https://vitepress.dev/reference/runtime-api#usedata)。

## 方程

$$
\begin{aligned}
\frac{\partial u}{\partial t} - \alpha \frac{\partial^2 u}{\partial x^2} &= 0, \quad x \in (0, 1), t > 0, \\
u(x, 0) &= \sin(\pi x), \\
u(0, t) &= u(1, t) = 0.
\end{aligned}
$$
