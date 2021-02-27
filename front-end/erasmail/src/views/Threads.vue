<template>
    <div>
        <Navbar></Navbar>
        <div class="section">
            <div class="columns">
                <div class="column has-text-centered logo">
                    EDGAR
                </div>
                <div class="column has-text-centered logo">
                    SAMIR
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

export default {
    name: "Home",
    data() {
        return {
            threads: null,
        };
    },
    computed: {
        ...mapGetters("auth", ["loggedIn"]),

    },
    components: {
        Navbar,
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
                    console.log(response.data)
                    this.threads = response.data
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    },
}
</script>

<style scoped>
.logo {
  padding: 5%;
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}
</style>