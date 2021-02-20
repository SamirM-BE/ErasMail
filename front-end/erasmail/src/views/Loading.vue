<template>
  <div>
    <div class="hero is-fullheight">
      <div class="hero-body">
        <div class="container">
          <div class="columns is-centered">
            <div class="column is-one-third has-text-centered">
              <p>Analyzing your emails</p>
              <ProgressbarEmail></ProgressbarEmail>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
import { mapGetters } from "vuex";
import ProgressbarEmail from "../components/ProgressbarEmail";

export default {
  computed: mapGetters("auth", ["loggedIn"]),
  components: {
    ProgressbarEmail,
  },
  created() {
    if (this.loggedIn) {
      getAPI
        .post(
          "/api/emails/",
          {
            app_password: this.$store.state.auth.app_password,
            host: this.$store.state.auth.host,
          },
          {
            headers: {
              Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
            },
          }
        )
        .then(() => {
          this.$router.push({
            name: "home",
          });
        })
        .catch((err) => {
          console.log(err);
        });
    }
  },
};
</script>

<style>
</style>