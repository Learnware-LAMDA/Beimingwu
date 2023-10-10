interface UserState {
  isEditing: boolean;
}

const user = {
  isEditing: false,
  getters: {
    getIsEditing(state: UserState): boolean {
      return state.isEditing;
    },
  },
  mutations: {
    setIsEditing(state: UserState, value: boolean): void {
      state.isEditing = value;
    },
  },
};

export default user;
