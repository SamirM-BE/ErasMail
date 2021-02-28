<template>
    <Navbar></Navbar>
    <div class="hero is-fullheight-with-navbar">
        <div class="hero-body">
            <div class="section p-0"> 
                <EmailModal :showModal="showModalFlag" :emails="emails" @hideModal="showModalFlag = false"></EmailModal>
                <div class="columns">
                    <div class="column is-half has-border p-0">
                        <div class="is-scrollable">
                            <ThreadBox v-for="(thread, idx) in threads" v-bind:key="idx" @click="showModal(thread.children)"
                                :subject="thread.subject" :size="thread.size"></ThreadBox>
                        </div>
                    </div>
                    <div class="column is-half has-border p-0">
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
import EmailModal from "../components/EmailModal";

export default {
    name: "Home",
    data() {
        return {
            showModalFlag: false,
            emails: [],
            threads: JSON.parse(localStorage.getItem('threads')),
        };
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),

    },
    components: {
        Navbar,
        ThreadBox,
        EmailModal
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
    //                 this.threads = response.data.children

    //                 localStorage.setItem('threads', JSON.stringify(response.data.children))
    //                 console.log(JSON.parse(localStorage.getItem('threads')))
    //             })
    //             .catch((err) => {
    //                 console.log(err);
    //             });
    //     }
    // },
    methods: {
        showModal(emails) {
            this.showModalFlag = true
            this.emails = emails
        },
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