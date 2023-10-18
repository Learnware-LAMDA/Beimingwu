import { getProfile } from "../../request/user";

interface AuthState {
  loggedIn: boolean;
  userName: string;
}

const auth = {
  state: {
    loggedIn: false,
    userName: "",
  },
  mutations: {
    setLoggedIn(state: AuthState, loggedIn: boolean): void {
      state.loggedIn = loggedIn;
      if (loggedIn) {
        getProfile().then((res) => {
          state.userName = res.data.username;
        });
      } else {
        state.userName = "";
      }
    },
  },
  getters: {
    getLoggedIn(state: AuthState): boolean {
      return state.loggedIn;
    },
    getUserName(state: AuthState): string {
      return state.userName;
    },
  },
};

export default auth;
