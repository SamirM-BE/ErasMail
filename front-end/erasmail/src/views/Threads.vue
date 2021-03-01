<template>
<div>
    <Navbar></Navbar>
    <div class="hero is-fullheight-with-navbar is-clipped">
        <div class="hero-body">
            <div class="section p-0"> 
                <EmailModal :showModal="showModalFlag" :emails="emails" :threadSubject="threadSubject" @hide-modal="showModalFlag = false" @remove-emails="removeEmails"></EmailModal>
                <div class="columns"> <!-- v-show="threads" -->
                    <div class="column is-half has-border p-0">
                        <div class="is-scrollable">
                            <ThreadBox v-for="(thread, idx) in threadsSorted" v-bind:key="idx" @click="showModal(thread.subject, thread.children, idx)"
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
            threads: JSON.parse(localStorage.getItem('threads')), //null,
            showModalFlag: false,
            threadIndex: -1,
            threadSubject: '',
            emails: [],
        }
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),
        threadsSorted() {
            if (this.threads) {
                var threadsList = this.threads.children
                threadsList.sort((a, b) => b.size - a.size)
                return threadsList
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
                    // localStorage.setItem('threads', JSON.stringify(response.data))
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    },
    methods: {
        showModal(threadSubject, emails, idx) {
            this.showModalFlag = true
            this.threadSubject = threadSubject
            this.emails = emails
            this.threadIndex = idx
        },
        removeEmails(emails) {
            for (let i = emails.emailsIndexSize.length - 1; i >= 0; i--) {
                this.threads.children[this.threadIndex].size -= emails.emailsIndexSize[i][1]
                this.threads.children[this.threadIndex].children.splice(emails.emailsIndexSize[i][0], 1);
            }
            if (this.threads.children[this.threadIndex].children.length === 0) {
                this.threads.children.splice(this.threadIndex, 1);
            }

            getAPI
                .delete(
                    "/api/emails/", {
                        headers: {
                            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                        },
                        data: {
                            app_password: this.$store.state.auth.app_password,
                            host: this.$store.state.auth.host,
                            uids:emails.uids
                        }
                    }
                )
                .catch((err) => {
                    console.log(err);
                });
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