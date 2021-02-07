import {
    axiosBase,
    getAPI
} from '../axios-api'

export const auth = {
    namespaced: true,
    state: {
        accessToken: localStorage.getItem('token-access'),
        refreshToken: localStorage.getItem('token-refresh'),

    },
    getters: {
        loggedIn(state) {
            return state.accessToken != null
        },

    },
    mutations: {
        updateStorage(state, {
            access,
            refresh
        }) {
            localStorage.setItem('token-access', access)
            localStorage.setItem('token-refresh', refresh)
            state.accessToken = access
            state.refreshToken = refresh
        },
        updateAccess(state, access) {
            state.accessToken = access
        },
        destroyToken(state) {
            localStorage.removeItem('token-access')
            localStorage.removeItem('token-refresh')
            state.accessToken = null
            state.refreshToken = null
        }
    },
    actions: {
        // run the below action to get a new access token on expiration
        refreshToken(context) {
            return new Promise((resolve, reject) => {
                axiosBase.post('api/token-refresh/', {
                        refresh: context.state.refreshToken
                    }) // send the stored refresh token to the backend API
                    .then(response => { // if API sends back new access and refresh token update the store
                        console.log('New access successfully generated')
                        context.commit('updateAccess', response.data.access)
                        resolve(response.data.access)
                    })
                    .catch(err => {
                        console.log('error in refreshToken Task')
                        reject(err) // error generating new access and refresh token because refresh token has expired
                    })
            })
        },
        userLogout(context) {
            if (context.getters.loggedIn) {
                return new Promise((resolve, reject) => {
                    getAPI.post('/api/users/logout', {refresh: context.state.refreshToken}, {
                            headers: {
                                Authorization: `Bearer ${context.state.accessToken}`
                            }
                        })
                        .then(() => {
                            context.commit('destroyToken')
                            resolve()
                        })
                        .catch(err => {

                            reject(err)
                        })
                })
            }
        },
        userLogin(context, usercredentials) {
            return new Promise((resolve, reject) => {
                axiosBase.post('/api/users/login', {
                        email: usercredentials.email,
                        application_password: usercredentials.application_password,
                        host: usercredentials.host
                    })
                    .then(response => {
                        console.log(response.data)
                        context.commit('updateStorage', {
                            access: response.data.access,
                            refresh: response.data.refresh
                        })
                        resolve()
                    })
                    .catch(err => {

                        reject(err)
                    })
            })
        }
    }
}