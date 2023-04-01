import Vuex from 'vuex'

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
  }
})