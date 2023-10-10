interface ErrorState {
  showGlobalError: boolean;
  globalErrorMsg: string;
}

const error = {
  state: {
    showGlobalError: false,
    globalErrorMsg: "",
  },
  getters: {
    getShowGlobalError(state: ErrorState): boolean {
      return state.showGlobalError;
    },
    getGlobalErrorMsg(state: ErrorState): string {
      return state.globalErrorMsg;
    },
  },
  mutations: {
    setShowGlobalError(state: ErrorState, value: boolean): void {
      state.showGlobalError = value;
    },
    setGlobalErrorMsg(state: ErrorState, value: string): void {
      state.globalErrorMsg = value;
    },
  },
};

export default error;
