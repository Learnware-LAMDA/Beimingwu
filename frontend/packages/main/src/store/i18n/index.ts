import i18n, { type Language } from "../../i18n";
import dayjs from "dayjs";

interface I18nLocaleState {
  locale: Language;
}

const i18nLocale = {
  state: {
    locale: "zh-cn",
  },
  mutations: {
    setLocale(state: I18nLocaleState, locale: Language): void {
      state.locale = locale;
      i18n.global.locale.value = locale;
      dayjs.locale(locale);
    },
  },
  getters: {
    getLocale(state: I18nLocaleState): Language {
      return state.locale;
    },
  },
};

export default i18nLocale;
