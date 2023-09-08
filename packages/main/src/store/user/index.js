const user = {
  isEditing: false,
  getters: {
    getIsEditing(state) {
      return state.isEditing;
    },
  },
  mutations: {
    setIsEditing(state, value) {
      state.isEditing = value;
    },
  },
};

export default user;
