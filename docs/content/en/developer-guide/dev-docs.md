# Docs Dev Guide

## Directory Structure

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

## Environment Setup

1. Install `nvm`

```bash
# use curl:
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
# or use wget:
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
```

2. Install `node`

```bash
nvm install node
```

3. Install `pnpm`

```bash
npm install -g pnpm
```

4. Install Dependencies: Make sure you are in the project's root directory `Beiming-System/docs/`.

```bash
pnpm install
```

## Development

### Run Development Server

Run the following command to start the development server.

```bash
pnpm dev
```

If everything goes well, you will see the following output:

```bash
> vitepress dev docs

  vitepress v1.0.0-rc.21

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

Afterward, make changes to markdown files under the `content` directory, and the browser will automatically reload to display the changes.

### Adding Static Files

If you want to add static files like images, you can place them in the `Beiming-System/docs/content/public/` directory. Then, you can access them in markdown files like this:

```markdown
![image](/image.png)
```

### Setting Up Navigation and Sidebar

You should set up this according to the language. For example, if you want to set up navigation and sidebar for the `en` language, you should edit the `Beiming-System/docs/content/.vitepress/config/locales/en.ts` file.

### Other Configuration

You can find more configuration options in the [VitePress documentation](https://vitepress.dev).

## Deployment

Run the following command to build static files.

```bash
pnpm build
```

Static files will be generated in the `Beiming-System/docs/content/.vitepress/dist/` directory. You can deploy them to any static file server.