# Markdown 擴展示例

本頁面展示了 VitePress 提供的一些內建 Markdown 擴展功能。

## 語法高亮

VitePress 提供了由[Shiki](https://github.com/shikijs/shiki)提供支援的語法高亮功能，還包括行高亮等附加功能：

**輸入**

````
```js{4}
export default {
  data () {
    return {
      msg: '高亮顯示!'
    }
  }
}
```
````

**輸出**

```js{4}
export default {
  data () {
    return {
      msg: '高亮顯示!'
    }
  }
}
```

## 自定義容器

**輸入**

```md
::: info
這是信息框。
:::

::: tip
這是提示。
:::

::: warning
這是警告。
:::

::: danger
這是危險警告。
:::

::: details
這是詳情塊。
:::
```

**輸出**

::: info
這是信息框。
:::

::: tip
這是提示。
:::

::: warning
這是警告。
:::

::: danger
這是危險警告。
:::

::: details
這是詳情塊。
:::

## 更多

查看[Markdown 擴展的完整列表的文檔](https://vitepress.dev/guide/markdown)。
