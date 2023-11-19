interface showState {
  showExampleDialog: boolean;
}

const tips = {
  state: {
    showExampleDialog: true,
  },
  getters: {
    getShowExampleDialog(state: showState): boolean {
      return state.showExampleDialog;
    },
  },
  mutations: {
    setShowExampleDialog(state: showState, showExampleDialog: boolean): void {
      state.showExampleDialog = showExampleDialog;
    },
  },
  actions: {
    showExampleDialog({ commit }: { commit: (arg0: string, arg1: unknown) => void }): void {
      commit("setShowExampleDialog", true);
    },
    hideExampleDialog({ commit }: { commit: (arg0: string, arg1: unknown) => void }): void {
      commit("setShowExampleDialog", false);
    },
  },
};

export default tips;
