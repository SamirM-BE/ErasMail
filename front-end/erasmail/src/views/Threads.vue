<template>
    <div>
        <Navbar></Navbar>
        <div class="section">
            <div class="columns">
                <div class="column logo p-0">
                    <div v-for="n in 5" :key="n" class="thread_box">
                        I'm in a box.
                    </div>
                </div>
                <div class="column has-text-centered logo">
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

export default {
    name: "Home",
    data() {
        return {
            threads: null,
            thread1: {
                has_attachmemnt: false,
                size: 81956,
                subject: "Alerte de sécurité",
                emails: []
            }
        };
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),

    },
    components: {
        Navbar,
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
.thread_box {
    border-radius: 10px;
    padding: 3%;
    margin: 1%;
    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

.logo {
  padding: 5%;
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}
</style>