import { createI18n } from "vue-i18n";
import { zh, en } from "@beiming-system/locale";

const messages = {
  en,
  zh,
};
const language =
  JSON.parse(localStorage.getItem("vuex") || "{}")?.i18n?.locale ||
  (navigator.language || "en").toLocaleLowerCase();
const i18n = createI18n({
  legacy: false,
  locale: language.split("-")[0] || "en",
  fallbackLocale: "en",
  messages,
});

export default i18n;
