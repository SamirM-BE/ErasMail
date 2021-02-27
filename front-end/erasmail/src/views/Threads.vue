<template>
    <div>
        <Navbar></Navbar>
        <div>
            <columns>
            <p> Salut </p>
            </columns>
            
        </div>
    </div>

</template>


<script>
import {
    getAPI
} from "../axios-api";
import { mapGetters } from "vuex";
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
                    for (var i in response.data) {
                        response.data[i].forEach(function(elem, index) {
                            console.log(elem.attachments, index);
                        });
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    },
}

</script>
