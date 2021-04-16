<template>

  <div class="container main-menu">
    <div class="columns is-centered">
      <div class="column c1 is-3">
        <FlippingCard :backData="'Delete some e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${userStats.emails_before_count} emails older than 3 years.`"
                      :frontTitle="'Old unread e-mails'"
                      @click="$router.push({name: 'emails', query: {unseen: true, before_than: 3}})"/>
      </div>
      <div class="column c2 is-3 is-offset-1">
        <FlippingCard
            :backData="`These emails will generate ${userStats.thread_carbon_yforecast} grams of co2 for every additional year they are stored. Delete some e-mails or attachments, save the nature !`"
            :backTitle="`These e-mails have so far polluted as much as ${getCO2equivalent(userStats.thread_co2)}.`"
            :frontData="`You have ${userStats.threads_count} threads with a total of ${attachmentCount} attachments with potential duplicates.`"
            :frontTitle="'Threads'"
            @click="routePage('threads')"/>
      </div>
      <div class="column c3 is-3 is-offset-1">
        <FlippingCard
            :backData="`These newsletters will generate XXX grams of co2 for every additional year they are stored. Unsubscribe from some newsletters, save the nature !`"
            :backTitle="`These newsletters have so far polluted as much as XXX.`"
            :frontData="`You have ${userStats.newsletters_count} different newsletters.`"
            :frontTitle="'Newsletters'"
            @click="routePage('newsletters')"/>
      </div>
    </div>


    <div class="columns is-centered pt-6">
      <div class="column c4 is-3">
        <FlippingCard :backData="'Delete your e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${userStats.emails_larger_count} e-mails larger than 2MB.`"
                      :frontTitle="'Large e-mails'"
                      @click="$router.push({name: 'emails', query: {greater_than: 2}})"/>
      </div>
      <div class="column c5 is-3 is-offset-1"> <!--TODO ! -->
        <FlippingCard :backData="'Delete your e-mails, save the nature !'"
                      :backTitle="'This is equivalent to 300 plastics bags'"
                      :frontData="`You have ${uselessCount} useless e-mails. (Calendar e-mails, reminder e-mails, empty e-mails)`"
                      :frontTitle="'Useless e-mails'"
                      @click="$router.push({name: 'emails', query: { 'selected_filters[]': ['reminder', 'welcome', 'invitation', 'meeting', 'verification', 'update', 'confirmation', 'social', 'no_reply']}})"/>
      </div>
      <div class="column c6 is-3 is-offset-1">
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

import FlippingCard from "../components/FlippingCard.vue";
import {getOptimalComparison} from "@/utils/pollution";

export default {
  name: "Home",
  components: {
    FlippingCard,
  },
  data() {
    return {
      userStats: {},
      attachmentCount: 256,
      uselessCount: 1546,
    };
  },
  created() {
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
      })
      .catch((err) => {
        console.log(err);
      });
  },
  methods: {
    routePage(path) {
      this.$router.push({
        name: path
      })
    },
    getCO2equivalent(carbon) {
      let equivalent = getOptimalComparison(carbon)
      if (equivalent.comparison)
        return `${equivalent.comparison.msg}.`
      return ""
    },
    getCO2YearlyForecast() {

    }
  },
};
</script>

<style scoped>

</style>
