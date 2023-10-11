interface AuthState {
  loggedIn: boolean;
}

const auth = {
  loggedIn: false,
  mutations: {
    setLoggedIn(state: AuthState, loggedIn: boolean): void {
      state.loggedIn = loggedIn;
    },
  },
  getters: {
    getLoggedIn(state: AuthState): boolean {
      return state.loggedIn;
    },
  },
};

export default auth;
