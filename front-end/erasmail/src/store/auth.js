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
            // localStorage.removeItem('token-access')
            // localStorage.removeItem('token-refresh')
            // localStorage.removeItem('app-password')
            // localStorage.removeItem('host')
            localStorage.clear()
            state.accessToken = null
            state.refreshToken = null
            state.app_password = null
            state.host = null
        }
    },
    actions: {
        // run the below action to get a new access token on expiration
        refreshToken(context) {
            // return new Promise((resolve, reject) => {
            return axiosBase.post('api/token-refresh/', {
                    refresh: context.state.refreshToken
                }) // send the stored refresh token to the backend API
                .then(response => { // if API sends back new access and refresh token update the store
                    console.log('New access successfully generated')
                    context.commit('updateAccess', response.data.access)
                    return response.data.access
                })
                .catch(err => {
                    console.log(`Error return while trying to refresh the token in vueX: ${err}`)
                    return err // error generating new access and refresh token because refresh token has expired
                })
            // })
        },
        userLogout(context) {
            if (context.getters.loggedIn) {
                let promise_delete_emails = getAPI.delete('/api/emails/', {
                    headers: {
                        Authorization: `Bearer ${context.state.accessToken}`
                    }
                })
                let promise_user_logout = getAPI.post('/api/users/logout', {
                    refresh: context.state.refreshToken
                }, {
                    headers: {
                        Authorization: `Bearer ${context.state.accessToken}`
                    }
                })
                let promise_destroy_auth = new Promise((resolve) => {
                    context.commit('destroyAuth')
                    console.log("The local storage has been flushed")
                    resolve()
                })
                return Promise.all([promise_delete_emails, promise_user_logout, promise_destroy_auth])
                    .catch(err => {
                        console.log(`Error return while trying to execute userLogout : ${err}`)
                        context.commit('destroyAuth')
                        return err
                    })
            }
        },
        userLogin(context, usercredentials) {
            // return new Promise((resolve, reject) => {
            return axiosBase.post('/api/users/login', {
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
                })
                .catch(err => {
                    console.log(`Error return while trying to execute userLogin : ${err}`)
                })
            // })
        }
    }
}