export default {
  label: "中文",
  lang: "zh-CN",
  themeConfig: {
    logo: "/logo.svg",
    nav: [
      { text: "🏠 首页", link: "/zh-CN/" },
      { text: "🌰 示例", link: "/zh-CN/overview/system-overview" },
    ],

    sidebar: [
      {
        text: "整体概览",
        items: [
          { text: "北冥系统介绍", link: "/zh-CN/overview/system-overview" },
          { text: "快速上手", link: "/zh-CN/overview/quick-start" },
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
              { text: "如何准备一个学件？", link: "/zh-CN/user-guide/learnware-upload" },
              { text: "如何上传学件？", link: "/zh-CN/user-guide/learnware-upload" },
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
          { text: "项目结构与开发规范", link: "/zh-CN/developer-guide/structure-and-guidelines" },
          {
            text: "系统快速部署",
            collapsed: true,
            items: [
              { text: "单机本地部署", link: "/zh-CN/developer-guide/deploy/local-deploy" },
              { text: "多机 Kubernetes 部署", link: "/zh-CN/developer-guide/deploy/k8s-deploy" },
            ],
          },
          { text: "前端开发指南", link: "/zh-CN/developer-guide/dev-frontend" },
          { text: "后端开发指南", link: "/zh-CN/developer-guide/dev-backend" },
          { text: "文档开发指南", link: "/zh-CN/developer-guide/dev-docs" },
        ],
      },
      {
        text: "版本公告",
        link: "/zh-CN/markdown-examples"
      },
      {
        text: "常见问题",
        link: "/zh-CN/markdown-examples"
      },
      {
        text: "联系我们",
        link: "/zh-CN/markdown-examples"
      },
    ],

    socialLinks: [
      { icon: "github", link: "https://github.com/vuejs/vitepress" },
    ],
  },
};
