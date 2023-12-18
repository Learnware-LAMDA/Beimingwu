import { createI18n } from "vue-i18n";
import { zhCn, en } from "@beiming-system/locale";

const messages = {
  en,
  "zh-cn": zhCn,
};

const i18n = createI18n({
  legacy: false,
  locale:
    JSON.parse(localStorage.getItem("vuex") || "{}")?.i18n?.locale ||
    (navigator.language || "en").toLocaleLowerCase() ||
    "en",
  fallbackLocale: "en",
  messages,
});

export type LanguageName = "en" | "zh-cn";
export type LanguageTitle = "English" | "中文";
export interface Language {
  name: LanguageName;
  title: LanguageTitle;
}

export const languages: Language[] = [
  {
    name: "en",
    title: "English",
  },
  {
    name: "zh-cn",
    title: "中文",
  },
];

export default i18n;
