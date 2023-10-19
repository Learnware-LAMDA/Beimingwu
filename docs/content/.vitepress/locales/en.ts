import type { LocaleSpecificConfig } from "vitepress";

const en: LocaleSpecificConfig & {
  label: string;
  link?: string;
  changeLang?: string;
} = {
  label: "English",
  lang: "en",
  changeLang: "Language",
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "Home", link: "/", icon: "mdi-home" },
      { text: "Examples", link: "/markdown-examples", icon: "mdi-collage" },
      { text: "System", link: "https://www.lamda.nju.edu.cn/learnware", icon: "mdi-domain"},
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

    outline: { label: "Outline" },

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],
  },
};

export default en;
