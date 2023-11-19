interface State {
  shownExampleTips: boolean;
}

const tips = {
  state: {
    shownExampleTips: false,
  },
  getters: {
    getShownExampleTips(state: State): boolean {
      return state.shownExampleTips;
    },
  },
  mutations: {
    setShowExampleTips(state: State, shownExampleTips: boolean): void {
      state.shownExampleTips = shownExampleTips;
    },
  },
  actions: {
    showExampleTips({ commit }: { commit: (name: string, value: boolean) => void }): void {
      commit("setShowExampleTips", true);
    },
  },
};

export default tips;
