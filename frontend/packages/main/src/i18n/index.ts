import { createI18n } from "vue-i18n";
import { zhCn, en } from "@beiming-system/locale";

const messages = {
  en,
  "zh-cn": zhCn,
};

const language =
  JSON.parse(localStorage.getItem("vuex") || "{}")?.i18n?.locale ||
  (navigator.language || "en").toLocaleLowerCase();

const i18n = createI18n({
  legacy: false,
  locale: language || "en",
  fallbackLocale: "en",
  messages,
});

export default i18n;
