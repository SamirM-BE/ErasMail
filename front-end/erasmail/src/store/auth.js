import {axiosBase, getAPI} from '../axios-api'

export const auth = {
    namespaced: true,
    state: {
        email: null,
        accessToken: null,
        refreshToken: null,
        app_password: null,
        host: null,
        smtpHost: null,
        smtpPort: null
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
            host,
            smtpHost,
            smtpPort
        }) {
            state.accessToken = access
            state.refreshToken = refresh
            state.app_password = app_password
            state.host = host
            state.smtpHost = smtpHost
            state.smtpPort = smtpPort
        },
        updateAccess(state, access) {
            state.accessToken = access
        },
        updateEmail(state, email) {
            state.email = email
        },
        destroyAuth(state) {
            state.email =  null
            state.accessToken = null
            state.refreshToken = null
            state.app_password = null
            state.host = null
            state.smtpHost = null
            state.smtpPort = null
        }
    },
    actions: {
        updateEmail(context, email) {
            return context.commit('updateEmail', email)
        },
        // run the below action to get a new access token on expiration
        refreshToken(context) {
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
                    context.dispatch('stats/destroyStats', null, {root: true})
                    context.dispatch('success/destroySuccess', null, {root: true})
                    context.commit('destroyAuth')
                })
        },
        userLogout(context) {
            if (context.getters.loggedIn) {
                getAPI.delete('/api/emails/', {
                    headers: {
                        Authorization: `Bearer ${context.state.accessToken}`
                    }
                })
                    .then(() => {
                        return getAPI.post('/api/users/logout', {
                            refresh: context.state.refreshToken
                        }, {
                            headers: {
                                Authorization: `Bearer ${context.state.accessToken}`
                            }
                        })
                    })
                    .then(() => {
                        context.dispatch('stats/destroyStats', null, {root: true})
                        context.dispatch('success/destroySuccess', null, {root: true})
                        context.commit('destroyAuth')
                    })
                    .catch(err => {
                        console.log(`Error return while trying to execute userLogout : ${err}`)
                        context.commit('destroyAuth')
                        context.dispatch('stats/destroyStats', null, { root: true })
                        context.dispatch('success/destroySuccess', null, { root: true })
                        return err
                    })
            }

            // if (context.getters.loggedIn) {
            //     let promise_delete_emails = getAPI.delete('/api/emails/', {
            //         headers: {
            //             Authorization: `Bearer ${context.state.accessToken}`
            //         }
            //     })
            //     let promise_user_logout = getAPI.post('/api/users/logout', {
            //         refresh: context.state.refreshToken
            //     }, {
            //         headers: {
            //             Authorization: `Bearer ${context.state.accessToken}`
            //         }
            //     })
            //     let promise_destroy_auth = new Promise((resolve) => {
            //         context.commit('destroyAuth')
            //         resolve()
            //     })
            //     return Promise.all([promise_delete_emails, promise_user_logout, promise_destroy_auth])
            //         .catch(err => {
            //             console.log(`Error return while trying to execute userLogout : ${err}`)
            //             context.commit('destroyAuth')
            //             return err
            //         })
            // }
        },
        userLogin(context, usercredentials) {
            return axiosBase.post('/api/users/login', {
                email: usercredentials.email,
                app_password: usercredentials.app_password,
                host: usercredentials.host
            })
                .then(response => {
                    context.commit('updateStorage', {
                        access: response.data.token['access'],
                        refresh: response.data.token['refresh'],
                        app_password: usercredentials.app_password,
                        host: usercredentials.host,
                        smtpHost: usercredentials.smtpHost,
                        smtpPort: usercredentials.smtpPort
                    })
                })
        }
    }
}