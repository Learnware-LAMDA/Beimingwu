export default {
  label: "中文",
  lang: "zh-CN",
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "🏠 首页", link: "/zh-Hans/" },
      { text: "🌰 示例", link: "/zh-Hans/markdown-examples" },
    ],

    sidebar: [
      {
        text: "示例",
        items: [
          { text: "Markdown 示例", link: "/zh-Hans/markdown-examples" },
          { text: "运行时 API 示例", link: "/zh-Hans/api-examples" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],
  },
};
