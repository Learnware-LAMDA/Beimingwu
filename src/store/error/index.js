const error = {
  state: {
    showGlobalError: false,
    globalErrorMsg: '',
  },
  getters: {
    getShowGlobalError(state) {
      return state.showGlobalError;
    },
    getGlobalErrorMsg(state) {
      return state.globalErrorMsg;
    },
  },
  mutations: {
    setShowGlobalError(state, value) {
      state.showGlobalError = value;
    },
    setGlobalErrorMsg(state, value) {
      state.globalErrorMsg = value;
    },
  },
};

export default error;
