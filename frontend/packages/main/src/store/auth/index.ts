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
    },
    setUserName(state: AuthState, userName: string): void {
      state.userName = userName;
    },
  },
  actions: {
    async login({ commit }: { commit: (arg0: string, arg1: unknown) => void }): Promise<void> {
      const res = await getProfile();
      commit("setLoggedIn", true);
      commit("setUserName", res.data.username);
    },
    async logout({ commit }: { commit: (arg0: string, arg1: unknown) => void }): Promise<void> {
      commit("setLoggedIn", false);
      commit("setUserName", "");
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
