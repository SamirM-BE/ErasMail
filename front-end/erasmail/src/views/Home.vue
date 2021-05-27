<template>

  <div class="container main-menu">
    <div class="columns is-centered">
      <div class="column c1 is-3">
        <FlippingCard
            :backData="`These emails will generate ${readableCo2(userStats.emails.emails_older_3Y_carbon_yforecast)} of co2 for every additional year they are stored. Delete some emails !`"
            :backTitle="`These emails have so far polluted as much as ${getCO2equivalent(userStats.emails.emails_older_3Y_carbon)}`"
            :frontData="`You have ${userStats.emails.emails_older_3Y_count} emails that are older than 3 years.`"
            :frontTitle="'Old emails'"
            @click="$router.push({name: 'emails', query: {before_than: 3}})"/>
      </div>
      <div class="column c2 is-3 is-offset-1">
        <FlippingCard
            :backData="`These emails will generate ${readableCo2(userStats.threads.carbon_yearly_forecast)} of co2 for every additional year they are stored. Delete some emails or attachments !`"
            :backTitle="`These emails have so far polluted as much as ${getCO2equivalent(userStats.threads.carbon)}`"
            :frontData="`You have ${userStats.threads.total} threads with a total of ${attachmentCount} attachments with potential duplicates.`"
            :frontTitle="'Threads'"
            @click="routePage('threads')"/>
      </div>
      <div class="column c3 is-3 is-offset-1">
        <FlippingCard
            :backData="`These newsletters will generate ${readableCo2(userStats.newsletters.carbon_yearly_forecast)} of co2 for every additional year they are stored. Unsubscribe from some newsletters !`"
            :backTitle="`These newsletters have so far polluted as much as ${getCO2equivalent(userStats.newsletters.carbon)}`"
            :frontData="`You have ${userStats.newsletters.total} different newsletters.`"
            :frontTitle="'Newsletters'"
            @click="routePage('newsletters')"/>
      </div>
    </div>


    <div class="columns is-centered pt-6">
      <div class="column c4 is-3">
        <FlippingCard
            :backData="`These emails will generate ${readableCo2(userStats.emails.emails_larger_1MB_carbon_yforecast)} of co2 for every additional year they are stored. Delete some emails !`"
            :backTitle="`These emails have so far polluted as much as ${getCO2equivalent(userStats.emails.emails_larger_1MB_carbon)}`"
            :frontData="`You have ${userStats.emails.emails_larger_1MB_count} emails larger than 1 MB.`"
            :frontTitle="'Large emails'"
            @click="$router.push({name: 'emails', query: {greater_than: 2}})"/>
      </div>
      <div class="column c5 is-3 is-offset-1"> <!--TODO ! -->
        <FlippingCard
            :backData="`These emails will generate ${readableCo2(userStats.emails.emails_useless_carbon_yforecast)} of co2 for every additional year they are stored. Delete some emails !`"
            :backTitle="`These emails have so far polluted as much as ${getCO2equivalent(userStats.emails.emails_useless_carbon)}`"
            :frontData="`You have ${userStats.emails.emails_useless_count} useless emails. (Reminders, welcome emails, social, ...)`"
            :frontTitle="'Useless emails'"
            @click="$router.push({name: 'emails', query: { 'selected_filters[]': ['reminder', 'welcome', 'invitation', 'meeting', 'verification', 'update', 'confirmation', 'social', 'no_reply']}})"/>
      </div>
      <div class="column c6 is-3 is-offset-1">
        <FlippingCard
            :backData="'Delete your emails !'"
            :frontData="'Find useless emails based on more than a dozen of filters.'"
            :frontTitle="'Advanced filters'"
            @click="routePage('emails')"/>

      </div>
    </div>
  </div>
</template>

<script>
const convert = require('convert-units');

import FlippingCard from "../components/FlippingCard.vue";
import {getOptimalComparison} from "@/utils/pollution";

export default {
  name: "Home",
  components: {
    FlippingCard,
  },
  data() {
    return {
      // userStats: {},
      attachmentCount: 256,
      uselessCount: 1546,
    };
  },
  computed: {
    userStats() {
      return this.$store.state.stats.statistics
    },
  },
  created() {
    console.log(this.userStats)
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
    readableCo2(co2) {
      co2 = convert(co2).from('g').toBest({
        exclude: ['mcg', 'mg', 'oz', 'lb', 'mt']
      })
      return `${Math.round(co2.val)} ${co2.unit}`
    },
  },
};
</script>

<style scoped>
.container {
  width: 100%;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>
