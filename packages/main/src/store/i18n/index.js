import i18n from "../../i18n";

const i18nLocale = {
  state: {
    locale: "cn",
  },
  mutations: {
    setLocale(state, locale) {
      state.locale = locale;
      i18n.global.locale.value = locale;
    },
  },
  getters: {
    getLocale(state) {
      return state.locale;
    },
  },
};

export default i18nLocale;
