<template>

  <div class="container main-menu">
    <div class="columns is-centered">
      <div class="column c1 is-2">
        <FlippingCard backData="'Delete some e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${userStats.emails_before_count} unread emails older than 3 years.`"
                      :frontTitle="'Old unread e-mails'"
                      @click="routePage('threads')"/>
      </div>
      <div class="column c2 is-2 is-offset-1">
        <FlippingCard :backData="'Delete some e-mails or some attachments, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${userStats.threads_count} threads with a total of ${attachmentCount} attachments with potential duplicates.`"
                      :frontTitle="'Threads'"
                      @click="routePage('threads')"/>
      </div>
      <div class="column c3 is-2 is-offset-1">
        <FlippingCard :backData="'Unsubscribe from the newsletters and delete their old e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${userStats.newsletters_count} different newsletters.`"
                      :frontTitle="'Newsletters'"
                      @click="routePage('threads')"/>
      </div>
    </div>


    <div class="columns is-centered pt-6">
      <div class="column c4 is-2">
        <FlippingCard :backData="'Delete your e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${userStats.emails_lighter_count} e-mails larger than 2MB.`"
                      :frontTitle="'Large e-mails'"
                      @click="routePage('threads')"/>
      </div>
      <div class="column c5 is-2 is-offset-1"> <!--TODO ! -->
        <FlippingCard :backData="'Delete your e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${uselessCount} useless e-mails. (Calendar e-mails, reminder e-mails, empty e-mails)`"
                      :frontTitle="'Useless e-mails'"
                      @click="routePage('threads')"/>
      </div>
      <div class="column c6 is-2 is-offset-1">
        <FlippingCard :backData="'Delete your e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="'Find useless emails based on more than a dozen of smart filters.'"
                      :frontTitle="'Smart clean'"
                      @click="routePage('threads')"/>

      </div>
    </div>
  </div>
</template>

<script>
import {getAPI} from "../axios-api";
import {mapGetters} from "vuex";

import FlippingCard from "../components/FlippingCard.vue";


export default {
  name: "Home",
  data() {
    return {
      userStats: {},
      attachmentCount: 256,
      uselessCount: 1546,
    };
  },
  computed: mapGetters("auth", ["loggedIn"]),
  components: {
    FlippingCard,
  },
  methods: {
    routePage(path) {
      this.$router.push({
        name: path
      })
    }
  },
  created() {
    if (this.loggedIn) {
      getAPI
          .get(
              "/api/emails/stats/user", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then((response) => {
            this.userStats = response.data
            console.log(this.userStats)
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
