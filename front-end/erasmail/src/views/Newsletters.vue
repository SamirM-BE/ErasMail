<template>
  <AwarenessMessage :co2="totalCarbon" :itemCount="newslettersCount" :itemName="'newsletters'"/>

  <div class="container newsletters">
    <div v-for="(newsletter, index) in newsletters" :key="index" class="field">
      {{ isUnsubscribed(index)}}
      <transition name="fade">
        <div v-if="newsletter && (!newsletter.unsubscribed || newsletter.emails_cnt !== 0)" class="box control px-0">
          <div class="newsletter-detail px-2 is-flex is-justify-content-space-between">
            <div class="leftpart">
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
            <div class="buttontop">
              <button v-if="!newsletter.unsubscribed" class="button is-small  is-info p-1"
                      @click="unsubscribe(index)">Unsubscribe
              </button>

              <span v-else class="tag is-fixed-corner-bottom is-success is-light is-rounded ml-1">
                <span class="icon">
                  <i class="far fa-thumbs-up"></i>
                </span>
                Unsubscribed
              </span>

              <button v-if="newsletter.emails_cnt !== 0"
                      class="button is-small  is-danger ml-1 p-1"
                      @click="deleteEmails(index)">Delete emails
              </button>
              <span v-else class="tag is-fixed-corner-bottom is-danger is-light is-rounded ml-1">
                <span class="icon">
                  <i class="far fa-thumbs-up"></i>
                </span>
                Deleted
              </span>

              <br>
              <button v-if="(!newsletter.unsubscribed && newsletter.emails_cnt !== 0)"
                      :class="{ 'is-hidden': newsletter.emails_cnt === 0 }"
                      class="button is-fullwidth is-small  is-success mt-1"
                      @click="unsubscribe(index); deleteEmails(index); fadeMe()">Unsubscribe & Delete
              </button>



            </div>
          </div>

        </div>


      </transition>

    </div>
    <!--    </form>-->
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
      totalCarbon: 0,
      showDeleteButton: [],
      show: true,
    };
  },
  computed: {
    newslettersCount() {
      return Object.keys(this.newsletters).length !== 0 ? this.newsletters.length : 0;
    },

  },
  components: {
    AwarenessMessage
  },
  methods: {
    fetchNewsletters() {
      console.log("fetch des newsletters")
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
    fadeMe: function () {
      console.log("aaaaaaaaaaaa")
      this.show = !this.show
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
      this.totalCarbon = pollution
    },
    parseMailTo(s) {
      var r = {};
      var email = s.match(/mailto:([^?]*)/);
      email = email[1] ? email[1] : false;
      var subject = s.match(/subject=([^&]+)/);
      subject = subject ? subject[1].replace(/\+/g, ' ') : false;

      if (email) {
        r['email'] = email;
      }
      if (subject) {
        r['subject'] = subject;
      }

      return r;
    },
    deleteEmails(clickedNewsletter) {

      let newsletter
      let sender_emails = []

      this.showDeleteButton[clickedNewsletter] = false
      newsletter = this.newsletters[clickedNewsletter]
      sender_emails.push(newsletter.sender_email)
      this.newsletters[clickedNewsletter].emails_cnt = 0
      this.newsletters[clickedNewsletter].seen_emails_cnt = 0


      // delete this.newsletters[clickedNewsletter]
      //TODO: AVOID ONE REQUEST BY NEWSLETTER
      getAPI
          .delete(
              "/api/emails/newsletters", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
                data: {
                  senders: sender_emails,
                  uids_to_delete: newsletter.uids_folders,
                  host: this.$store.state.auth.host,
                  app_password: this.$store.state.auth.app_password
                }
              }
          )
          .then(() => {
            delete this.newsletters[clickedNewsletter].uids_folders
          })
          .catch((err) => {
            console.log(err);
          });
    },
    // if no email is received from more than 3 months we consider the newsletter as unsubscribed
    isUnsubscribed(clickedNewsletter){
      let lastReceptionDate = new Date(this.newsletters[clickedNewsletter].received_at)
      let today = new Date()
      if( (today.getMonth() - lastReceptionDate.getMonth() + (12 * (today.getFullYear() - lastReceptionDate.getFullYear())))>3)
        this.newsletters[clickedNewsletter].unsubscribed = true
    },
    unsubscribe(clickedNewsletter) {
      let newsletter = []

      let request_data = {}

      this.newsletters[clickedNewsletter].unsubscribed = true
      this.newsletters[clickedNewsletter].forecasted_carbon = 0
      newsletter = this.newsletters[clickedNewsletter]
      request_data["id"] = newsletter.id

      //ONE-CLICK
      if (newsletter.one_click) {
        // unsubscribe_type = "oneclick"
        request_data["unsubscribe_type"] = "oneclick"
        request_data["url"] = newsletter.list_unsubscribe
      }
      //MAILTO
      else if (newsletter.list_unsubscribe.substring(0, 6) === "mailto") {
        request_data["unsubscribe_type"] = "mailto"
        var mailtoParams = this.parseMailTo(newsletter.list_unsubscribe)
        request_data["to"] = mailtoParams['email']
        request_data["subject"] = mailtoParams['subject']
        request_data["host"] = this.$store.state.auth.host
        request_data["app_password"] = this.$store.state.auth.app_password

      }
      //MANUAL
      else {
        window.open(newsletter.list_unsubscribe, '_blank');
      }
      getAPI
          .post(
              "/api/emails/newsletters/unsubscribe",
              request_data,
              {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then(() => {
            console.log("Successfull unsubscribe")
          })
          .catch((err) => {
            console.log(err.response);
          });
      //}
      // }

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


.control {
  display: flex;
  align-items: center;
  border-color: lightgray !important;
  border: solid;
  border-width: thin;

}

.is-size-6-2 {
  font-size: 0.85rem;
}

.newsletter-detail {
  width: 100%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s
}

.fade-enter,
.fade-leave-to
  /* .fade-leave-active in <2.1.8 */

{
  opacity: 0
}

.is-fixed-corner-bottom {
  position: absolute;
  bottom: 20%;
  right: 0.2%;
}


</style>