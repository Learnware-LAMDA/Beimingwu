import { getProfile } from "../../request/user";

interface AuthState {
  loggedIn: boolean;
  userName: string;
  role: number;
}

const auth = {
  state: {
    loggedIn: false,
    userName: "",
    role: 0,
  },
  mutations: {
    setLoggedIn(state: AuthState, loggedIn: boolean): void {
      state.loggedIn = loggedIn;
    },
    setUserName(state: AuthState, userName: string): void {
      state.userName = userName;
    },
    setRole(state: AuthState, role: number): void {
      state.role = role;
    },
  },
  actions: {
    async login({ commit }: { commit: (arg0: string, arg1: unknown) => void }): Promise<void> {
      const res = await getProfile();
      commit("setLoggedIn", true);
      commit("setUserName", res.data.username);
      commit("setRole", res.data.role);
    },
    async logout({ commit }: { commit: (arg0: string, arg1: unknown) => void }): Promise<void> {
      commit("setLoggedIn", false);
      commit("setUserName", "");
      commit("setRole", 0);
    },
  },
  getters: {
    getLoggedIn(state: AuthState): boolean {
      return state.loggedIn;
    },
    getUserName(state: AuthState): string {
      return state.userName;
    },
    getRole(state: AuthState): number {
      return state.role;
    },
  },
};

export default auth;
