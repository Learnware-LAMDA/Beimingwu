import type { LocaleSpecificConfig } from "vitepress";

const en: LocaleSpecificConfig & {
  label: string;
  link?: string;
  changeLang?: string;
} = {
  label: "English",
  lang: "en",
  title: "Beimingwu Docs",
  changeLang: "Language",
  themeConfig: {
    logo: "/logo-no-text.svg",
    nav: [
      { text: "Home", link: "/en/", icon: "mdi-home" },
      {
        text: "Guide",
        link: "/en/overview/system-overview",
        icon: "mdi-collage",
      },
      { text: "System", link: "https://www.bmwu.cloud", icon: "mdi-domain" },
    ],

    sidebar: [
      {
        text: "Overview",
        items: [
          { text: "System Overview", link: "/en/overview/system-overview" },
          { text: "Quick Start", link: "/en/overview/quick-start" },
          { text: "Installation", link: "/en/overview/installation" },
        ],
        collapsed: false,
      },
      {
        text: "User Guide",
        collapsed: false,
        items: [
          {
            text: "Learnware Upload",
            collapsed: true,
            items: [
              {
                text: "Learnware Preparation",
                link: "/en/user-guide/learnware-upload/prepare",
              },
              {
                text: "Upload via Web Interface",
                link: "/en/user-guide/learnware-upload/upload-web",
              },
              {
                text: "Upload via Client Interface",
                link: "/en/user-guide/learnware-upload/upload-client",
              },
            ],
          },
          { text: "Learnware Search", link: "/en/user-guide/learnware-search" },
          { text: "Learnware Deployment", link: "/en/user-guide/learnware-deploy" },
        ],
      },
      {
        text: "System Dev Guide",
        collapsed: false,
        items: [
          {
            text: "Project Structure and Guidelines",
            link: "/en/developer-guide/structure-and-guidelines",
          },
          {
            text: "Quick System Deployment",
            collapsed: true,
            items: [
              {
                text: "Local Deployment",
                link: "/en/developer-guide/deploy/local-deploy",
              },
              {
                text: "Multi-Node Kubernetes Deployment",
                link: "/en/developer-guide/deploy/k8s-deploy",
              },
            ],
          },
          { text: "Frontend Dev Guide", link: "/en/developer-guide/dev-frontend" },
          { text: "Backend Dev Guide", link: "/en/developer-guide/dev-backend" },
          { text: "Docs Dev Guide", link: "/en/developer-guide/dev-docs" },
        ],
      },
      {
        text: "User Agreement",
        link: "/en/user-agreement",
      },
      {
        text: "Privacy Policy",
        link: "/en/privacy-policy",
      },
      {
        text: "Version Announcement",
        link: "/en/versions",
      },
      {
        text: "Common Questions",
        link: "/en/common-questions",
      },
      {
        text: "About Us",
        link: "/en/about-us",
      },
    ],

    outline: { label: "Outline" },

    socialLinks: [
      { icon: "git", link: "https://www.gitlink.org.cn/beimingwu/beimingwu" },
      { icon: "github", link: "https://github.com/learnware-lamda/Beimingwu" },
    ],
  },
};

export default en;
