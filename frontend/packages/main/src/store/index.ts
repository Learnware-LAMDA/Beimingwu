import Vuex from "vuex";
import VuexPersistence from "vuex-persist";
import auth from "./auth";
import error from "./error";
import user from "./user";
import i18n from "./i18n";
import deployTips from "./deployTips";

export default new Vuex.Store({
  modules: {
    auth,
    error,
    user,
    i18n,
    deployTips,
  },
  plugins: [new VuexPersistence().plugin],
});
