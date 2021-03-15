<template>
  <div>
    <SuccessNotification :notification_message="'You have successfully logged in'">
    </SuccessNotification>
    <section class="section is-flex is-justify-content-center">
      <div class="container">
        <div class="columns is-centered is-vcentered mb15">
          <div class="column is-4 has-text-centered logo">
            <strong> ErasMail </strong>
          </div>
          <div class="column is-5">
            <strong class="title">Welcome to ErasMail</strong>
            <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Veniam consequatur omnis quasi cum impedit
              ipsum
              amet sapiente libero beatae, enim voluptatibus velit perferendis, atque sunt soluta architecto, quo
              debitis alias!</p>
          </div>
        </div>
        <div class="columns is-centered">
          <div class="column is-4 has-text-centered">
            <p>Analyzing your emails</p>
            <ProgressbarEmail></ProgressbarEmail>
          </div>
        </div>
        <div class="columns is-centered">
          <div class="column has-text-centered">
            <p>{{ awareness_messages[index] }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import {getAPI} from "../axios-api";
import {mapGetters} from "vuex";
import ProgressbarEmail from "../components/ProgressbarEmail";
import SuccessNotification from "../components/SuccessNotification";

const display_time = 7; // display time of awareness messages in seconds

const awareness_messages = [
  "Compress your files before sending them",
  "Avoid thank-you emails",
  "Deleting 30 emails is equivalent to saving 24 hours of the consumption of a light bulb",
  "Avoid replying to all recipients when not necessary",
  "Download your attachments and delete associated emails whenever possible",
];

export default {
  data() {
    return {
      counter: Math.floor(Math.random() * awareness_messages.length),
      awareness_messages: awareness_messages,
    };
  },
  mounted() {
    setInterval(() => {
      this.counter++;
    }, 1000 * display_time);
  },
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
    index() {
      return this.counter % this.awareness_messages.length;
    },
  },
  components: {
    ProgressbarEmail,
    SuccessNotification,
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

<style scoped>
.mb15 {
  margin-bottom: 15%;
}

.logo {
  padding: 5%;
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}

.section {
  width: 100%;
}
</style>