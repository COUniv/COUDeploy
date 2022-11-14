const state = {
  listVisible: true
}

const getters = {
  listVisible: (state) => {
    return state.listVisible
  }
}

const mutations = {
  toggleVisible (state) {
    if (state.listVisible === true) {
      state.listVisible = false
    } else {
      state.listVisible = true
    }
  }
}

export default {
  state,
  getters,
  mutations
}
