import {createStore} from 'vuex'
import {auth} from './auth'
import {stats} from './stats'
import {success} from './success'

import createPersistedState from "vuex-persistedstate";

export default createStore({
    modules: {
        auth,
        stats,
        success,
    },
    plugins: [createPersistedState()],
})