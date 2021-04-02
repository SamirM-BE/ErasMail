<template>
  <!--  <div>-->
<!--  newslettersCount-->
  <AwarenessMessage :co2="totalCarbon" :itemCount="50" :itemName="'newsletters'"/>

  <div class="container">
    <div class="buttons is-pulled-right my-1">
      <button class="button is-focused is-link mx-1" @click="unsubscribe()">Unsubscribe</button>
      <button class="button is-focused is-danger mx-1" @click="deleteEmails()">Delete emails</button>
      <button class="button is-focused is-danger is-light  mx-1" @click="unsubscribe(); deleteEmails()">Unsubscribe &
        delete
      </button>
    </div>
  </div>

  <div class="container newsletters">
    <form>
      <div v-for="(newsletter, index) in newsletters" :key="index" class="field">
        <div class="box control px-0">
          <input :id="index" v-model="checkedNewsletters" :value="index" type="checkbox">
          <label :for="index" class="checkbox">
            <div class="newsletter-detail has-border-left px-2">

              <div class="icon-text">
                  <span class="icon">
                      <i class="far fa-address-card fa-sm"></i>
                  </span>

                <span class="is-size-6">{{ newsletter.sender_name }}
                    <span v-if="newsletter.sender_name" class="is-size-6-2">
                      ({{ newsletter.sender_email }})
                    </span>
                    <span v-else>{{ newsletter.sender_email }}</span>
                  </span>
              </div>

              <span class="icon-text has-text-link" title="Number of stored emails from this mailing list">
                <span class="icon">
                  <i class="fas fa-envelope"></i>
                </span>
                <span>{{ newsletter.emails_cnt }}</span>
              </span>

              <span class="icon-text has-text-info pl-5" title="Open rate for this mailing list">
                <span class="icon">
                  <i class="fas fa-eye"></i>
                </span>
                <span>{{ getNewsletterOpenRate(newsletter) }}%</span>
              </span>

              <span class="icon-text has-text-danger pl-5"
                    title="Forecast of the number of emails you will receive this year based on the number of emails you have already received.">
                <span class="icon">
                  <i class="fas fa-inbox"></i>
                </span>
                <span>{{ Math.round(newsletter.avg_daily_emails * 365.25) }}</span>
              </span>
              <p class="has-text-weight-bold">Last email received : {{ newsletter.received_at }}</p>
            </div>
          </label>

        </div>
      </div>
    </form>
  </div>

</template>

<script>
import {getAPI} from "@/axios-api";
import AwarenessMessage from "../components/AwarenessMessage";

export default {
  name: "Newsletters",
  data() {
    return {
      newsletters: {},
      checkedNewsletters: [],
      totalCarbon: 0.0,
    };
  },
  computed: {
    newslettersCount() {
      return this.newsletters.length
    },

  },
  components: {
    AwarenessMessage
  },
  methods: {
    fetchNewsletters() {
      getAPI
          .get(
              "/api/emails/newsletters", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then((response) => {
            this.newsletterPollution(response.data)
            this.newsletters = response.data
          })
          .catch((err) => {
            console.log(err);
          });
    },
    getNewsletterOpenRate(newsletter) {
      if (newsletter.emails_count !== 0 && newsletter.seen_emails_cnt !== 0) {
        let open_rate = newsletter.seen_emails_cnt / newsletter.emails_cnt * 100
        open_rate = open_rate.toPrecision(3)
        return open_rate
      } else
        return 0
    },
    newsletterPollution(newsletters) {
      let pollution = 0.0
      if (newsletters) {

        pollution = newsletters.reduce((a, b) => a + (b['generated_carbon'] || 0), 0);
      }
      this.totalCarbon =  pollution
    },
  },
  created() {
    this.fetchNewsletters()
  }
}
</script>

<style scoped>
input {
  margin: 1%;
}

.has-border-left {
  border-left-width: thin !important;
  border-left: solid;
}

.box.control {
  display: flex;
  align-items: center;
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}

.is-size-6-2 {
  font-size: 0.85rem;
}
</style>