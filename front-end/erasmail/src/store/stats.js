import {getAPI} from "@/axios-api";
import axios from "axios";


export const stats = {
    namespaced: true,
    state: {
        statistics: {},
    },
    mutations: {
        setInitialState(state, statistics) {
            state.statistics = statistics
        },
        updateStatistic(state, statToUpdate) {
            state.statistics.erasmail[statToUpdate.stat] = statToUpdate.value
        },
        destroyStats(state) {
            Object.assign(state.statistics, {})
        },
    },
    actions: {
        //Get initial state from database through API
        getInitialState(context) {

            //email stats
            const requestInitialStats = getAPI
                .get(
                    "/api/emails/stats/user", {
                        headers: {
                            Authorization: `Bearer ${context.rootState.auth.accessToken}`,
                        },
                    }
                )

            //user stats
            const requestConnectedCount = getAPI.get(
                "/api/users/me", {
                    headers: {
                        Authorization: `Bearer ${context.rootState.auth.accessToken}`,
                    },
                }
            )

            return axios.all([requestConnectedCount, requestInitialStats])
                .then((responses) => {
                    var stats = {...responses[0].data, ...responses[1].data} //stats will contain email stats + user stats (connected_count)
                    context.commit('setInitialState', stats)
                })
                .catch((err) => {
                    console.log(err);
                });


        },

        updateStatistics(context, statsToUpdate) {
            for (const id of statsToUpdate['ids']) {
                //pute type parameter and then statistics[type][id]
                context.commit('updateStatistic', {
                    stat: id,
                    value: context.state.statistics.erasmail[id] + statsToUpdate['value']
                })
            }
        },

        //reset statistics on logout
        destroyStats(context) {
            context.commit('destroyStats')
        },
    }
}