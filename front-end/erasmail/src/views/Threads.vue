<template>
<div>
    <Navbar></Navbar>
    <div class="hero is-fullheight-with-navbar">
        <div class="hero-body">
            <div class="section p-0">
                <div class="columns">
                    <div class="column is-half has-border p-0">
                        <div class="is-scrollable">
                            <ThreadBox v-for="(thread, idx) in threads.children" v-bind:key="idx"
                                :subject="thread.subject" :size="thread.size"></ThreadBox>
                        </div>
                    </div>
                    <div class="column is-half has-border p-0">
                        <div class="is-scrollable">
                            <Treemap :threads_prop="threads"> </Treemap>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</div>
</template>


<script>
import {
    getAPI
} from "../axios-api";
import {
    mapGetters
} from "vuex";
import Navbar from "../components/Navbar";
import ThreadBox from "../components/ThreadBox";
import Treemap from "../components/Treemap";

export default {
    name: "Home",
    data() {
        return {
            threads: null, 
            threads_raw: localStorage.getItem('threads_raw')
        };
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),

    },
    components: {
        Navbar,
        ThreadBox,
        Treemap,
    },
    created() {
        if (this.loggedIn) {
            getAPI
                .get(
                    "/api/emails/threads", {
                        headers: {
                            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                        },
                    }
                ).then((response) => {
                    this.threads = response.data
                    console.log(response.data)
                    console.log(this.threads)
                    localStorage.setItem('threads_raw', JSON.stringify(response.data))
                })
                .catch((err) => {
                    console.log(err);
                });
        }
        
    },
}
</script>

<style scoped>
.section {
    width: 100%;
}

.column {
    height: 75vh;
}

.is-scrollable {
    overflow: auto;
    height: 100%;
}

.has-border {
    border-color: lightgray !important;
    border: solid;
    border-width: thin;
}
</style>