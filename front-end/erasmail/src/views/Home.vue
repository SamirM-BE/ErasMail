<template>
  <div>
    <Navbar></Navbar>
    <h1 v-if="!loggedIn">{{ $t('views.home.publicContent') }}</h1>
    <h1 v-else>{{ $t('views.home.privateContent', { email: email }) }}</h1>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
import { mapGetters } from "vuex";
import Navbar from "../components/Navbar";

export default {
  name: "Home",
  data() {
    return {
      email: null,
    };
  },
  computed: mapGetters("auth", ["loggedIn"]),
  components: {
    Navbar,
  },
  created() {
    if (this.loggedIn) {
      getAPI
        .get("/api/users/me", {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
        })
        .then((response) => {
          this.email = response.data.email;
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
};
</script>

<style scoped>
</style>
