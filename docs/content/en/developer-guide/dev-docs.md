# 系统文档开发

## 目录结构

<details open>
  <summary>/</summary>
  <ul>
    <li>.eslintignore</li>
    <li>.eslintrc.cjs</li>
    <li>.prettierignore</li>
    <li>.prettierrc</li>
    <li>README.md</li>
    <li>
      <details>
        <summary>content</summary>
        <ul>
          <li>
            <details>
              <summary>.vitepress</summary>
              <ul>
                <li>
                  <details>
                    <summary>components</summary>
                    <ul>
                      <li>LocalSearchBox.vue</li>
                      <li>NavBar.vue</li>
                      <li>NavBarMenuLink.vue</li>
                      <li>NavBarTranslations.vue</li>
                    </ul>
                  </details>
                </li>
                <li>
                  <details>
                    <summary>composables</summary>
                    <ul>
                      <li>index.ts</li>
                    </ul>
                  </details>
                </li>
                <li>config.ts</li>
                <li>
                  <details>
                    <summary>configs</summary>
                    <ul>
                      <li>index.ts</li>
                      <li>
                        <details>
                          <summary>locales</summary>
                          <ul>
                            <li>en.ts</li>
                            <li>index.ts</li>
                            <li>zh-CN.ts</li>
                          </ul>
                        </details>
                      </li>
                      <li>
                        <details>
                          <summary>search</summary>
                          <ul>
                            <li>index.ts</li>
                            <li>stopwords.ts</li>
                            <li>translate.ts</li>
                          </ul>
                        </details>
                      </li>
                    </ul>
                  </details>
                </li>
                <li>mathjax.ts</li>
                <li>shim.d.ts</li>
              </ul>
            </details>
          </li>
          <li>api-examples.md</li>
          <li>
            <details>
              <summary>developer-guide</summary>
              <ul>
                <li>dev-docs.md</li>
              </ul>
            </details>
          </li>
          <li>index.md</li>
          <li>markdown-examples.md</li>
          <li>
            <details>
              <summary>public</summary>
              <ul>
                <li>image.jpg</li>
                <li>logo.svg</li>
              </ul>
            </details>
          </li>
          <li>tsconfig.json</li>
          <li>
            <details>
              <summary>zh-CN</summary>
              <ul>
                <li>api-examples.md</li>
                <li>
                  <details>
                    <summary>developer-guide</summary>
                    <ul>
                      <li>
                        <details>
                          <summary>deploy</summary>
                          <ul>
                            <li>k8s-deploy.md</li>
                            <li>local-deploy.md</li>
                          </ul>
                        </details>
                      </li>
                      <li>dev-backend.md</li>
                      <li>dev-docs.md</li>
                      <li>dev-frontend.md</li>
                      <li>structure-and-guidelines.md</li>
                    </ul>
                  </details>
                </li>
                <li>index.md</li>
                <li>markdown-examples.md</li>
                <li>
                  <details>
                    <summary>overview</summary>
                    <ul>
                      <li>installation.md</li>
                      <li>quick-start.md</li>
                      <li>system-overview.md</li>
                    </ul>
                  </details>
                </li>
                <li>
                  <details>
                    <summary>user-guide</summary>
                    <ul>
                      <li>learnware-deploy.md</li>
                      <li>learnware-search.md</li>
                      <li>
                        <details>
                          <summary>learnware-upload</summary>
                          <ul>
                            <li>prepare.md</li>
                            <li>upload.md</li>
                          </ul>
                        </details>
                      </li>
                    </ul>
                  </details>
                </li>
              </ul>
            </details>
          </li>
        </ul>
      </details>
    </li>
    <li>package.json</li>
    <li>pnpm-lock.yaml</li>
  </ul>
</details>

## 环境搭建

1. 安装 `nvm`

```bash
# use curl:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
# or use wget:
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
```

2. 安装 `node`

```bash
nvm install node
```

3. 安装 `pnpm`

```bash
npm install -g pnpm
```

4. 安装依赖
   确保你在项目的根目录 `Beiming-System/docs/` 下。

```bash
pnpm install
```

## 开发

### 运行开发服务器

运行以下命令来启动开发服务器。

```bash
pnpm dev
```

如果一切顺利，你应该看到以下输出：

```bash
> vitepress dev docs

  vitepress v1.0.0-rc.21

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

之后，更改 `content` 目录下的 markdown 文件，浏览器将自动重新加载以显示更改。

### 添加静态文件

如果你想添加静态文件，比如图片，你可以把它们放在 `Beiming-System/docs/content/public/` 目录下。然后你可以在 markdown 文件中这样访问它们：

```markdown
![image](/image.png)
```

### 设置导航栏和侧边栏

你应该按语言设置。例如，如果你想为 `en` 语言设置导航栏和侧边栏，你应该编辑 `Beiming-System/docs/content/.vitepress/config/locales/en.ts` 文件。

### 其他配置

你可以在 [VitePress 文档](https://vitepress.dev) 中找到更多配置。

## 部署

运行以下命令来构建静态文件。

```bash
pnpm build
```

静态文件将生成在 `Beiming-System/docs/content/.vitepress/dist/` 目录下。你可以将它们部署到任何静态文件服务器。
