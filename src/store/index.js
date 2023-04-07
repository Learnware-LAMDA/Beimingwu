import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'
import auth from './auth'
import error from './error'

export default new Vuex.Store({
  modules: {
    auth,
    error
  },
  plugins: [new VuexPersistence().plugin],
})