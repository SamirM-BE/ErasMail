<template>
  <SuccessNotification :notification_message="'You have successfully logged in'">
  </SuccessNotification>
  <section class="section erasmail">
    <div class="columns is-centered is-vcentered">
      <div class="column is-4 has-text-centered logo">
        <strong> ErasMail </strong>
      </div>
      <div class="column is-5">
        <div class="content">
          <h1><strong>Welcome to <span class="has-text-primary">ErasMail &#127758;</span></strong></h1>
          <p>Erasmail comes with a bunch of tools and features that will help you quickly and efficiently reduce the environmental impact of your mailboxes</p>
        </div>
      </div>
    </div>
  </section>
  <section class="section mx-6">
    <p class="has-text-centered is-size-4 has-text-black">Explore what you can do</p>
    <br>
    <div class="columns">
      <div class="column is-one-third" v-for="(feature, idx) in featuresToShow" :key="idx">
        <div class="box content has-background-success-light py-6">
          <h4 class="has-text-centered has-text-link">{{feature.name}}</h4>
          <br>
          <p class="is-uppercase is-size-7 has-text-justified">{{feature.content}}</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section progress-bar is-flex is-flex-direction-column is-align-items-center">
    <p>Analyzing your emails</p>
    <progress class="progress is-small is-primary my-1" max="100"></progress>
    <p>{{ awareness_messages[index] }}</p>

    <div class="icon-text has-text-grey-light mt-4">
      <span class="icon">
        <i class="fa fa-exclamation-triangle"></i>
      </span>
      <span>The deleted emails are moved to trash folder !!</span>
      <span class="icon">
        <i class="fa fa-exclamation-triangle"></i>
      </span>
    </div>
  </section>

</template>

<script>
import {getAPI} from "../axios-api";
import {useToast} from "vue-toastification";

import SuccessNotification from "../components/SuccessNotification";

const display_time_awareness = 7; // display time of awareness messages in seconds
const display_time_features = 10; // display time of features in seconds

const awareness_messages = [
  "Compress your files before sending them",
  "Avoid thank-you emails",
  "Deleting 30 emails is equivalent to saving 24 hours of the consumption of a light bulb",
  "Avoid replying to all recipients when not necessary",
  "Download your attachments and delete associated emails whenever possible",
];

const features = [{
    name: 'Threads',
    content: "Conversations are the best opportunity for duplicating useless attachments, let's clean up to reduce the ecological impact."
  },
  {
    name: 'Old Emails',
    content: "You'll probably never read again those old emails again, might as well delete them for the planet"
  },
  {
    name: 'Heavy Emails',
    content: "These emails weigh down your email box and ... also for the environment."
  },
  {
    name: 'Newsletter',
    content: "Do you really need all your newsletters? Let's see if it's not better to unsubscribe."
  },
  {
    name: 'Statistics',
    content: 'Monitor your progress and share it on your social media'
  },
]

export default {
  name: "Loading",
  components: {
    SuccessNotification,
  },
  data() {
    return {
      awareness_counter: Math.floor(Math.random() * awareness_messages.length),
      awareness_messages: awareness_messages,
      features: features,
      feature_counter: 0,
    };
  },
  created() {
    getAPI
      .post(
        "/api/emails/", {
          app_password: this.$store.state.auth.app_password,
          host: this.$store.state.auth.host,
        }, {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
        }
      )
      .then(() => {
        return this.fetchUserStats()
      })
      .then(() => {
        this.$router.push({
          name: "home",
        })
      })
      .catch((err) => {
        console.log(err);
        this.$store.dispatch('auth/userLogout')
          .then(() => {
            this.$router.push({
              name: 'login'
            })
          })
      })
  },
  mounted() {
    setInterval(() => {
      this.awareness_counter++;
    }, 1000 * display_time_awareness);
    setInterval(() => {
      this.feature_counter++;
    }, 1000 * display_time_features);
  },
  computed: {
    index() {
      return this.awareness_counter % this.awareness_messages.length;
    },
    featuresToShow() {
      let i = this.feature_counter % Math.ceil(this.features.length / 3.0);
      let start = i * 3;
      let finish = (i + 1) * 3
      return this.features.slice(start, finish)
    },
    successDetails() {
      return this.$store.state.success.successDetails
    }
  },
  methods: {
    showSuccess(success) {
      const toast = useToast();
      toast.success(`Unlocked success : ${success}`);
    },
    fetchUserStats() {
      return this.$store.dispatch("stats/getInitialState")
          .then(() => {

            //Check if user has unlocked the connected_count success
            let statToUpdate = 'connected_count'
            for (const success of this.successDetails[statToUpdate]) {
              if (this.$store.state.stats.statistics.connected_count === success.minValue && !success.done) {
                this.showSuccess(success.todo)
              }
            }
            this.$store.dispatch('success/updateAllSuccess',)
          })
    },
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
.progress {
  width: 30vw;
}
.box{
  height: 100%;
}
</style>