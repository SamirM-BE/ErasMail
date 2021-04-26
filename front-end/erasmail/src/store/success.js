import successDetails from '../success-data.json'

const getDefaultState = () => {
    return {
        successDetails: successDetails, //successDetails contains all the success of success-data.json
    }
}

export const success = {
    namespaced: true,
    state: getDefaultState(),

    getters: {

        // Flat the structure of the success details and add the id property to all the objects (previously as key object)
        // we need this flatten structure to avoid double for loop in templates.
        successList(state) {
            let successList = []
            for (const id in state.successDetails) {
                successList.push(...Object.values(state.successDetails[id]).map(success => ({...success, id: id})))
            }
            return successList
        },
    },
    mutations: {
        setSuccessDone(state, {id, currentValue,}) {
            //iterate over the 3 levels of success
            for (const success of state.successDetails[id]) {
                success.done = success.minValue <= currentValue
            }
        },
        destroySuccess(state) {
            Object.assign(state, getDefaultState())
        },
    },
    actions: {
        //check for each success the done condition, set done to true if condition OK
        setSuccessDone(context, id) {
            context.commit('setSuccessDone', {
                id: id,
                currentValue: context.rootState.stats.statistics.erasmail[id]
            })
        },
        updateAllSuccess(context) {
            //iterate over all success
            for (const id in context.state.successDetails) {
                context.dispatch('setSuccessDone', id)
            }
        },
        destroySuccess(context) {
            context.commit('destroySuccess')
        },
    }
}