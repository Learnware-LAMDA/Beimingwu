interface TipsState {
  shownTips: boolean;
}

const tips = {
  state: {
    shownTips: false,
  },
  getters: {
    getShownTips(state: TipsState): boolean {
      return state.shownTips;
    },
  },
  mutations: {
    setShownTips(state: TipsState, shownTips: boolean): void {
      console.log({ state });
      console.log(shownTips);
      state.shownTips = shownTips;
    },
  },
  actions: {
    showTips({ commit }: { commit: (arg0: string, arg1: unknown) => void }): void {
      commit("setShownTips", true);
    },
  },
};

export default tips;
