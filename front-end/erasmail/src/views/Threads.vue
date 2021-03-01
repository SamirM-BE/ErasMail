<template>
<div>
    <Navbar></Navbar>
    <div class="hero is-fullheight-with-navbar">
        <div class="hero-body">
            <div class="section p-0"> 
                <EmailModal :showModal="showModalFlag" :emails="emails" :threadSubject="threadSubject" @hide-modal="showModalFlag = false" @remove-emails="removeEmails"></EmailModal>
                <div class="columns"> <!-- v-show="threads" -->
                    <div class="column is-half has-border p-0">
                        <div class="is-scrollable">
                            <ThreadBox v-for="(thread, idx) in threadsList" v-bind:key="idx" @click="showModal(thread.subject, thread.children)"
                                :subject="thread.subject" :size="thread.size"></ThreadBox>
                        </div>
                    </div>
                    <div class="column is-half has-border p-0">
                        <!-- <div class="is-scrollable"> -->
                            <Treemap :threads_prop="threads"> </Treemap>
                        <!-- </div> -->
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
import EmailModal from "../components/EmailModal";

// TODO threads = response.data au lieu de response.data.children

export default {
    name: "Home",
    data() {
        return {
            threads: null,
            showModalFlag: false,
            threadSubject: '',
            emails: [],
        }
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),
        threadsList(){
            if(this.threads){
                return this.threads.children
            }
            return null
        }
    },
    components: {
        Navbar,
        ThreadBox,
        EmailModal,
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
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    },
    methods: {
        showModal(threadSubject, emails) {
            this.showModalFlag = true
            this.threadSubject= threadSubject
            this.emails = emails
        },
        removeEmails(emails) {
            console.log(`send remove request here ! ${JSON.stringify(emails)}`)
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