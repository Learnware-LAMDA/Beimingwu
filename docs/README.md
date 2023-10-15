# Beiming System Docs

## Setup

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

4. Install dependencies
   Make sure you are in the root directory `Beiming-System/docs/` of this project.

```bash
pnpm install
```

## Development

### Run a development server

Run the following command to start a development server.

```bash
pnpm dev
```

If everything goes well, you should see the following output:

```bash
> vitepress dev docs

  vitepress v1.0.0-rc.21

  ➜  Local:   http://127.0.0.1:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

After that, change a markdown file in the `content` directory, and the browser will automatically reload to show the changes.

### Add static files

If you want to add static files, such as images, you can put them in the `Beiming-System/docs/content/public/` directory. Then you can access them in the markdown file like this:

```markdown
![image](/image.png)
```

### Setup the navbar and the sidebar

You should setup language by language. For example, if you want to setup the navbar and the sidebar for the `en` language, you should edit the
`Beiming-System/docs/content/.vitepress/config/locales/en.ts` file.

### Other configurations

You can find more configurations in the [VitePress documentation](https://vitepress.dev).

## Deployment

Run the following command to build the static files.

```bash
pnpm build
```

The static files will be generated in the `Beiming-System/docs/content/.vitepress/dist/` directory. You can deploy them to any static file server.
