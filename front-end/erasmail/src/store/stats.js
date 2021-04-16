import {getAPI} from "@/axios-api";
import axios from "axios";

const getDefaultState = () => {
    return {
        mailbox_size: 0,
        carbon_eq_at_creation: 0.0,
        carbon_eq: 0.0,
        emails_count: 0,
        emails_seen_count: 0,
        emails_received_count: 0,
        months_since_creation: 0.0,
        saved_co2: 0.0,
        deleted_emails_count: 0,
        badges_shared: 0,
        stats_shared: 0,
        unsubscribed_newsletters_count: 0,
        newsletters_deleted_emails_count: 0,
        deleted_emails_olderF_count: 0,
        deleted_emails_largerF_count: 0,
        deleted_emails_useless_count: 0,
        threads_deleted_emails_count: 0,
        deleted_attachments_count: 0,
        connected_count: 0,
    }
}

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
            state.statistics[statToUpdate.stat] = statToUpdate.value
        },
        destroyStats(state) {
            Object.assign(state.statistics, getDefaultState())
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
                context.commit('updateStatistic', {
                    stat: id,
                    value: context.state.statistics[id] + statsToUpdate['value']
                })
            }
        },

        //reset statistics on logout
        destroyStats(context) {
            context.commit('destroyStats')
        },
    }
}