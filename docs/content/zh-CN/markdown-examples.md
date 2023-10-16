# Markdown 扩展示例

本页面展示了 VitePress 提供的一些内置 Markdown 扩展功能。

## 语法高亮

VitePress 提供了由[Shiki](https://github.com/shikijs/shiki)提供支持的语法高亮功能，还包括行高亮等附加功能：

**输入**

````
```js{4}
export default {
  data () {
    return {
      msg: '高亮显示!'
    }
  }
}
```
````

**输出**

```js{4}
export default {
  data () {
    return {
      msg: '高亮显示!'
    }
  }
}
```

## 自定义容器

**输入**

```md
::: info
这是信息框。
:::

::: tip
这是提示。
:::

::: warning
这是警告。
:::

::: danger
这是危险警告。
:::

::: details
这是详情块。
:::
```

**输出**

::: info
这是信息框。
:::

::: tip
这是提示。
:::

::: warning
这是警告。
:::

::: danger
这是危险警告。
:::

::: details
这是详情块。
:::

## 更多

查看[Markdown 扩展的完整列表的文档](https://vitepress.dev/guide/markdown)。
