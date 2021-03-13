<template>

  <div class="container main-menu">
    <div class="columns is-centered ">
      <div class="column c1 is-2">
        <FlippingCard @click="routePage('threads')" :frontTitle="'Old unread e-mails'"
          :frontData="`You have ${unreadCount} unread emails older than 3 years.`"
          :backTitle="'This is equivalent to 300 plastics bags'" :backData="'Delete some e-mails, save the nature !'" />
      </div>
      <div class="column c2 is-2 is-offset-1">
        <FlippingCard @click="routePage('threads')" :frontTitle="'Threads'"
          :frontData="`You have ${threadCount} threads with a total of ${attachmentCount} attachments with potential duplicates.`"
          :backTitle="'This is equivalent to 300 plastics bags'" :backData="'Delete some e-mails or some attachments, save the nature !'" />
      </div>
      <div class="column c3 is-2 is-offset-1">
        <FlippingCard @click="routePage('threads')" :frontTitle="'Newsletters'"
          :frontData="`You have ${newsletterCount} different newsletters.`"
          :backTitle="'This is equivalent to 300 plastics bags'" :backData="'Unsubscribe from the newsletters and delete their old e-mails, save the nature !'" />
      </div>
    </div>


    <div class="columns is-centered pt-6">
      <div class="column c4 is-2">
        <FlippingCard @click="routePage('threads')" :frontTitle="'Large e-mails'"
          :frontData="`You have ${largeCount} e-mails larger than 2MB.`"
          :backTitle="'This is equivalent to 300 plastics bags'" :backData="'Delete your e-mails, save the nature !'" />
      </div>
      <div class="column c5 is-2 is-offset-1">
        <FlippingCard @click="routePage('threads')" :frontTitle="'Useless e-mails'"
          :frontData="`You have ${uselessCount} useless e-mails. (Calendar e-mails, reminder e-mails, empty e-mails)`"
          :backTitle="'This is equivalent to 300 plastics bags'" :backData="'Delete your e-mails, save the nature !'" />
      </div>
      <div class="column c6 is-2 is-offset-1">
        <FlippingCard @click="routePage('threads')" :frontTitle="'Smart clean'"
          :frontData="'Find useless emails based on more than a dozen of smart filters.'"
          :backTitle="'This is equivalent to 300 plastics bags'" :backData="'Delete your e-mails, save the nature !'" />
      
      </div>
    </div>
  </div>
</template>

<script>
import { getAPI } from "../axios-api";
import { mapGetters } from "vuex";

import FlippingCard from "../components/FlippingCard2.vue";


export default {
  name: "Home",
  data() {
    return {
      email: null,
      unreadCount: 3515,
      threadCount: 53,
      attachmentCount: 256,
      newsletterCount: 45,
      largeCount: 785,
      uselessCount: 1546,
    };
  },
  computed: mapGetters("auth", ["loggedIn"]),
  components: {
    FlippingCard,
    // FlippingCard2
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
