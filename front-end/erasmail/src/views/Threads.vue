<template>
    <div>
        <Navbar></Navbar>
        <div class="section">
            <div class="columns">
                <div class="column is-half logo p-0">
                    <div class="thread_field">
                        <ThreadBox v-for="(thread, idx) in threads.children" v-bind:key="idx" :subject="thread.subject" :size="thread.size">
                    </ThreadBox>
                    </div>
                </div>
                <div class="column is-half logo p-0">
                    SAMIR
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
    //                 console.log(response.data)
    //                 this.threads = response.data
    //                 localStorage.setItem('threads', JSON.stringify(response.data))
    //                 var threads = localStorage.getItem('threads');
    //                 console.log(JSON.parse(threads))
    //             })
    //             .catch((err) => {
    //                 console.log(err);
    //             });
    //     }
    // },
}
</script>

<style scoped>
.logo {
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}
</style>