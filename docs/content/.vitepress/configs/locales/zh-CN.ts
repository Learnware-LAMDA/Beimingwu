import type { LocaleSpecificConfig } from "vitepress";

const zhCN: LocaleSpecificConfig & {
  label: string;
  link?: string;
  changeLang?: string;
} = {
  label: "中文",
  lang: "zh-CN",
  title: "北冥坞文档",
  changeLang: "语言",
  themeConfig: {
    logo: "/logo-no-text.svg",
    nav: [
      { text: "首页", link: "/zh-CN/", icon: "mdi-home" },
      {
        text: "指南",
        link: "/zh-CN/overview/system-overview",
        icon: "mdi-collage",
      },
      { text: "系统", link: "https://www.bmwu.cloud", icon: "mdi-domain" },
    ],

    sidebar: [
      {
        text: "整体概览",
        items: [
          { text: "系统介绍", link: "/zh-CN/overview/system-overview" },
          { text: "快速上手", link: "/zh-CN/overview/quick-start" },
          { text: "环境安装", link: "/zh-CN/overview/installation" },
        ],
        collapsed: false,
      },
      {
        text: "使用指南",
        collapsed: false,
        items: [
          {
            text: "学件上传",
            collapsed: true,
            items: [
              {
                text: "如何准备一个学件？",
                link: "/zh-CN/user-guide/learnware-upload/prepare",
              },
              {
                text: "通过网页端上传",
                link: "/zh-CN/user-guide/learnware-upload/upload-web",
              },
              {
                text: "通过客户端上传",
                link: "/zh-CN/user-guide/learnware-upload/upload-client",
              },
            ],
          },
          { text: "学件查搜", link: "/zh-CN/user-guide/learnware-search" },
          { text: "学件部署", link: "/zh-CN/user-guide/learnware-deploy" },
        ],
      },
      {
        text: "开发指南",
        collapsed: false,
        items: [
          {
            text: "项目结构与开发规范",
            link: "/zh-CN/developer-guide/structure-and-guidelines",
          },
          {
            text: "系统快速部署",
            collapsed: true,
            items: [
              {
                text: "单机本地部署",
                link: "/zh-CN/developer-guide/deploy/local-deploy",
              },
              {
                text: "多机 Kubernetes 部署",
                link: "/zh-CN/developer-guide/deploy/k8s-deploy",
              },
            ],
          },
          { text: "前端开发指南", link: "/zh-CN/developer-guide/dev-frontend" },
          { text: "后端开发指南", link: "/zh-CN/developer-guide/dev-backend" },
          { text: "文档开发指南", link: "/zh-CN/developer-guide/dev-docs" },
        ],
      },
      {
        text: "用户协议",
        link: "/zh-CN/user-agreement",
      },
      {
        text: "隐私政策",
        link: "/zh-CN/privacy-policy",
      },
      {
        text: "版本公告",
        link: "/zh-CN/versions",
      },
      {
        text: "常见问题",
        link: "/zh-CN/common-questions",
      },
      {
        text: "关于我们",
        link: "/zh-CN/about-us",
      },
    ],

    outline: { label: "大纲" },

    socialLinks: [{ icon: "github", link: "https://github.com/Learnware-LAMDA/Beiming-System" }],
  },
};

export default zhCN;
