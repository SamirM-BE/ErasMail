<template>

            <Navbar></Navbar>
        <div class="hero is-fullheight-with-navbar">
        <div class="hero-body">
            <div class="section p-0">
                <div class="columns">
                    <div class="column is-half logo p-0">
                        <div class="thread_field">
                            <ThreadBox v-for="(thread, idx) in threads.children" v-bind:key="idx"
                                :subject="thread.subject" :size="thread.size"></ThreadBox>
                            
                        </div>
                    </div>
                    <div class="column is-half logo p-0">
                        SAMIR
                    </div>
                </div>
            </div>
        </div>

    </div>

</template>


<script>
// import {
//     getAPI
// } from "../axios-api";
import {
    mapGetters
} from "vuex";
import Navbar from "../components/Navbar";
import ThreadBox from "../components/ThreadBox";

export default {
    name: "Home",
    data() {
        return {
            threads: JSON.parse(localStorage.getItem('threads')),
        };
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),

    },
    components: {
        Navbar,
        ThreadBox,
    },
    // created() {
    //     if (this.loggedIn) {
    //         getAPI
    //             .get(
    //                 "/api/emails/threads", {
    //                     headers: {
    //                         Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
    //                     },
    //                 }
    //             ).then((response) => {
    //                 this.threads = response.data

    //                 localStorage.setItem('threads', JSON.stringify(response.data))
    //                 console.log(JSON.parse(localStorage.getItem('threads')))
    //             })
    //             .catch((err) => {
    //                 console.log(err);
    //             });
    //     }
    // },
}
</script>

<style scoped>

.section {
    width: 100%;
}
.thread_field {
    overflow: auto;
    height: 100%;
}
.column {
    height: 50em;
}

.logo {
    border-color: lightgray !important;
    border: solid;
    border-width: thin;
}
</style>