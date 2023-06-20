const auth = {
  loggedIn: false,
  mutations: {
    setLoggedIn(state, loggedIn) {
      state.loggedIn = loggedIn;
    },
  },
  getters: {
    getLoggedIn(state) {
      return state.loggedIn;
    },
  },
};

export default auth;
