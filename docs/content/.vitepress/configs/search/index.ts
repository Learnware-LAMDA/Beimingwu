import type { DefaultTheme } from "vitepress";

const search: DefaultTheme.Config["search"] = {
  provider: "local",
  options: {
    miniSearch: {
      searchOptions: {
        fuzzy: 0,
        fields: ["title", "titles", "text"],
      },
    },
    locales: {
      "zh-CN": {
        translations: {
          button: {
            buttonText: "搜索文档",
            buttonAriaLabel: "搜索文档",
          },
          modal: {
            noResultsText: "无法找到相关结果",
            resetButtonTitle: "清除查询条件",
            footer: {
              selectText: "选择",
              navigateText: "切换",
            },
          },
        },
      },
    },
  },
};

export default search;
