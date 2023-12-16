interface DarkState {
  dark: boolean;
}

const dark = {
  state: {
    dark: false,
  },
  mutations: {
    setDark(state: DarkState, dark: boolean): void {
      state.dark = dark;
    },
  },
  getters: {
    getDark(state: DarkState): boolean {
      return state.dark;
    },
  },
  actions: {
    toggleDark({ commit, getters }: any): void {
      commit("setDark", !getters.getDark);
      document.documentElement.classList.toggle("dark");
    },
  },
};

export default dark;
