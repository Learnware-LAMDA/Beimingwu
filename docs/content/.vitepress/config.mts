import { defineConfig } from "vitepress";
import mathjax3 from "markdown-it-mathjax3";
import { customElement } from "./mathjax";
import locales from "./locales";
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
      ],
    },
  },
  themeConfig: {
    search: {
      provider: "local",
      options: {
        miniSearch: {
          options: {
            tokenize: (string) => string.split(" ").flatMap(word => /[\u4e00-\u9fa5]/.test(word) ? [...word] : [word]),
          },
          searchOptions: {
            fuzzy: 0.2,
            fields: ["title", "text"],
            tokenize: (string) => string.split(" ").flatMap(word => /[\u4e00-\u9fa5]/.test(word) ? [...word] : [word]),
          }
        },
        locales: {
          "zh-CN": {
            translations: {
              button: {
                buttonText: "搜索文档",
                buttonAriaLabel: "搜索文档"
              },
              modal: {
                noResultsText: "无法找到相关结果",
                resetButtonTitle: "清除查询条件",
                footer: {
                  selectText: "选择",
                  navigateText: "切换"
                }
              }
            }
          }
        }
      }
    }
  }
});
