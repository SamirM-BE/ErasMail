import {
    axiosBase,
    getAPI
} from '../axios-api'

export const auth = {
    namespaced: true,
    state: {
        accessToken: localStorage.getItem('token-access'),
        refreshToken: localStorage.getItem('token-refresh'),
        app_password: localStorage.getItem('app-password'),
        host: localStorage.getItem("host"),
    },
    getters: {
        loggedIn(state) {
            return state.accessToken != null
        },

    },
    mutations: {
        updateStorage(state, {
            access,
            refresh,
            app_password,
            host
        }) {
            localStorage.setItem('token-access', access)
            localStorage.setItem('token-refresh', refresh)
            localStorage.setItem('app-password', app_password)
            localStorage.setItem('host', host)
            state.accessToken = access
            state.refreshToken = refresh
            state.app_password = app_password
            state.host = host
        },
        updateAccess(state, access) {
            localStorage.setItem('token-access', access)
            state.accessToken = access
        },
        destroyAuth(state) {
            localStorage.removeItem('token-access')
            localStorage.removeItem('token-refresh')
            localStorage.removeItem('app-password')
            localStorage.removeItem('host')
            state.accessToken = null
            state.refreshToken = null
            state.app_password = null
            state.host = null
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
        async userLogout(context) {
            if (context.getters.loggedIn) {
                 const promise1 = await getAPI.delete('/api/emails/', {
                    headers: {
                        Authorization: `Bearer ${context.state.accessToken}`
                    }
                })
                // })
                const promise2 = await getAPI.post('/api/users/logout', { refresh: context.state.refreshToken }, {
                        headers: {
                            Authorization: `Bearer ${context.state.accessToken}`
                        }
                    }).then(() => {
                        context.commit('destroyAuth')

                    })
                


                Promise.all([promise1, promise2])

            }
        },
        userLogin(context, usercredentials) {
            return new Promise((resolve, reject) => {
                axiosBase.post('/api/users/login', {
                    email: usercredentials.email,
                    app_password: usercredentials.app_password,
                    host: usercredentials.host
                })
                    .then(response => {
                        console.log(response.data)
                        context.commit('updateStorage', {
                            access: response.data.access,
                            refresh: response.data.refresh,
                            app_password: usercredentials.app_password,
                            host: usercredentials.host
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