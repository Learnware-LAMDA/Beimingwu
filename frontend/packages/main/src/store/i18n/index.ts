import i18n, { type LanguageName } from "../../i18n";
import dayjs from "dayjs";

interface I18nLocaleState {
  locale: LanguageName;
}

const i18nLocale = {
  state: {
    locale: "zh-cn",
  },
  mutations: {
    setLocale(state: I18nLocaleState, locale: LanguageName): void {
      state.locale = locale;
      i18n.global.locale.value = locale;
      dayjs.locale(locale);
    },
  },
  getters: {
    getLocale(state: I18nLocaleState): LanguageName {
      return state.locale;
    },
  },
};

export default i18nLocale;
