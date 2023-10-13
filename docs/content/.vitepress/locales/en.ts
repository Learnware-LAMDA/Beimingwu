export default {
  label: "English",
  lang: "en",
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "🏠 Home", link: "/" },
      { text: "🌰 Examples", link: "/markdown-examples" },
    ],

    sidebar: [
      {
        text: "Examples",
        items: [
          { text: "Markdown Examples", link: "/markdown-examples" },
          { text: "Runtime API Examples", link: "/api-examples" },
        ],
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],
  },
};
