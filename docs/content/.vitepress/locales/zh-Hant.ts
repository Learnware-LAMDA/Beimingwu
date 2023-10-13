export default {
  label: "繁體中文",
  lang: "zh-TW",
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "🏠 首頁", link: "/zh-Hant/" },
      { text: "🌰 示例", link: "/zh-Hant/markdown-examples" },
    ],

    sidebar: [
      {
        text: "示例",
        items: [
          { text: "Markdown 示例", link: "/zh-Hant/markdown-examples" },
          { text: "運行時 API 示例", link: "/zh-Hant/api-examples" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],
  },
};
