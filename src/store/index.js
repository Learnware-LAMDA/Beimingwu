import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

export default new Vuex.Store({
  state: {
    loggedIn: false,
    user: {
      id: 0,
      username: '',
      email: '',
      role: '',
      token: ''
    },
  },
  getters: {
    getLoggedIn(state) {
      return state.loggedIn
    }
  },
  mutations: {
    setLoggedIn(state, loggedIn) {
      state.loggedIn = loggedIn
    },
    setUser(state, user) {
      state.user = user
    },
    clearUser(state) {
      state.user = {
        id: 0,
        username: '',
        email: '',
        role: '',
        token: ''
      }
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [new VuexPersistence().plugin],
})