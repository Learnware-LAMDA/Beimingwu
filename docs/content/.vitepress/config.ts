import { defineConfig } from "vitepress";
import mathjax3 from "markdown-it-mathjax3";
import { customElement } from "./mathjax";
import { locales, search } from "./configs";
import { fileURLToPath } from "url";

function replaceComponent(source: string | RegExp, target: string) {
  return {
    find: source,
    replacement: fileURLToPath(new URL(target, import.meta.url)),
  };
}

export default defineConfig({
  title: "Beiming",
  description: "A VitePress Site",
  locales,
  markdown: {
    config: (md) => {
      md.use(mathjax3);
    },
  },
  vue: {
    template: {
      compilerOptions: {
        isCustomElement: (tag) => customElement.includes(tag),
      },
    },
  },
  vite: {
    resolve: {
      alias: [
        replaceComponent(/^.*\/VPNavBarMenuLink\.vue$/, "./components/NavBarMenuLink.vue"),
        replaceComponent(/^.*\/VPNavBar\.vue$/, "./components/NavBar.vue"),
        replaceComponent(/^.*\/VPNavBarTranslations\.vue$/, "./components/NavBarTranslations.vue"),
        replaceComponent(/^.*\/VPLocalSearchBox\.vue$/, "./components/LocalSearchBox.vue"),
      ],
    },
  },
  themeConfig: { search },
  ignoreDeadLinks: true,
});
