<template>
  <div>
    <h1 v-if="!loggedIn">Public content</h1>
    <h1 v-else>Private content : {{ email }}</h1>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
import { mapGetters } from "vuex";

export default {
  name: "Home",
  data() {
    return {
      email: null,
    };
  },
  computed: mapGetters("auth", ["loggedIn"]),
  components: {
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
