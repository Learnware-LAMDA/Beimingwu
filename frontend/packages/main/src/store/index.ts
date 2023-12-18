import Vuex from "vuex";
import VuexPersistence from "vuex-persist";
import auth from "./auth";
import error from "./error";
import user from "./user";
import i18n from "./i18n";
import exampleTips from "./exampleTips";
import dark from "./dark";

export default new Vuex.Store({
  modules: {
    auth,
    error,
    user,
    i18n,
    exampleTips,
    dark,
  },
  plugins: [new VuexPersistence().plugin],
});
