interface State {
  exampleTipsCount: number;
}

const tips = {
  state: {
    exampleTipsCount: 0,
  },
  getters: {
    getShowExampleTips(state: State): boolean {
      return state.exampleTipsCount <= 3;
    },
  },
  mutations: {
    incrementExampleTips(state: State): void {
      state.exampleTipsCount += 1;
    },
  },
  actions: {
    showExampleTips({ commit }: { commit: (name: string) => void }): void {
      commit("incrementExampleTips");
    },
  },
};

export default tips;
