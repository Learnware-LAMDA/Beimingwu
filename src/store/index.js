import Vuex from "vuex";
import VuexPersistence from "vuex-persist";
import auth from "./auth";
import error from "./error";
import user from "./user";

export default new Vuex.Store({
  modules: {
    auth,
    error,
    user,
  },
  plugins: [new VuexPersistence().plugin],
});
