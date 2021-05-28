<template>
  <AwarenessMessage :co2="totalCarbon" :forecastCarbon="totalForecastedCarbon"
                    :forecastMsg="`Keeping these newsletters for one more additional year will generate as much CO2 as `"
                    :itemCount="newslettersCount"
                    :itemName="'newsletters'"/>
  <!--  <div class="notification is-success">-->
  <!--    <button class="delete"></button>-->
  <!--    Unlocked Success : Connect to ErasMail two different days !-->
  <!--  </div>-->
  <div class="container newsletters mb-4">
    <div v-for="(newsletter, index) in newsletters" :key="index" class="field">
      {{ isUnsubscribed(index) }}
      <transition name="fade">
        <div v-if="newsletter && (!newsletter.unsubscribed || newsletter.emails_cnt !== 0)" class="box control px-0"
        >
          <div class="newsletter-detail px-2 is-flex is-justify-content-space-between" @mouseleave="hover = -1"
               @mouseover="hover = index">
            <div class="leftpart">
              <div class="icon-text">
                  <span class="icon">
                      <i class="far fa-address-card fa-sm"></i>
                  </span>
                <!--                generated_carbon forecasted_carbon-->
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
              <p class="has-text-weight-bold">Last received email: {{ newsletter.received_at }}</p>
              <ThreeBestComparison :co2="newsletter.generated_carbon" :show="hover===index"
                                   title="The carbon footprint of this conversation is the same as:"/>
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

            <!--            <p v-show="hover && newsletter.forecasted_carbon" class="is-italic is-size-7">-->
            <!--              Keeping this conversation for one more additional year will generate as much CO2 as {{newsletter.forecasted_carbon}}-->
            <!--            </p>-->

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
import ThreeBestComparison from "../components/ThreeBestComparison";
import {useToast} from "vue-toastification";

export default {
  name: "Newsletters",
  components: {
    AwarenessMessage,
    ThreeBestComparison,
  },
  data() {
    return {
      newsletters: [],
      showDeleteButton: [],
      show: true,
      hover: false,

      newslettersCount: 0,
      totalCarbon: 0,
      totalForecastedCarbon: 0,
      nextPageNumber: 1,

      ready: false, // whether ready to fetch new data from the backend
    };
  },
  created() {
    this.fetchNextNewsletters().then(() => {
      this.ready = true
    })
  },
  mounted() {
    window.onscroll = () => {
      let bottomOfWindow = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop) + window.innerHeight >= Math.round(document.documentElement.offsetHeight * 0.95)
      if (bottomOfWindow && this.ready) {
        this.ready = false
        let response = this.fetchNextNewsletters()
        if (response) {
          response.then(() => {
            this.ready = true
          })
        }
      }
    }
  },
  computed: {
    // unsubscribed_count() {
    //   return this.$store.state.stats.unsubscribed_newsletters_count
    // },
    // deleted_count() {
    //   return this.$store.state.stats.newsletters_deleted_emails_count
    // },
    successDetails() {
      return this.$store.state.success.successDetails
    },
  },
  methods: {
    fetchNextNewsletters() {
      if (!this.nextPageNumber) {
        // if there is no page to retrieve then don't query the backend
        return
      }
      return getAPI
          .get(
              "/api/emails/newsletters", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
                params: {
                  page: this.nextPageNumber,
                }
              }
          )
          .then((response) => {
            this.newslettersCount = response.data.count
            this.totalCarbon = response.data.carbon
            this.totalForecastedCarbon = response.data.carbon_yearly_forecast
            if(this.nextPageNumber === 1){
              this.newsletters = response.data.results
            } else {
              this.newsletters.push(...response.data.results)
            }
            if (response.data.next) {
              this.nextPageNumber = new URL(response.data.next).searchParams.get('page')
            } else {
              this.nextPageNumber = null
            }
          })
          .catch((err) => {
            console.log(err);
          });
    },
    fadeMe: function () {
      this.show = !this.show
    },
    checkNotification(isUnsubscribe) {
      let statToUpdate
      if (isUnsubscribe) {
        statToUpdate = 'unsubscribed_newsletters'
      } else {
        statToUpdate = 'deleted_emails_newsletters_feature'
      }
      for (const success of this.successDetails[statToUpdate]) {
        if (this.$store.state.stats.statistics.erasmail[statToUpdate] >= success.minValue && !success.done)
          this.showSuccess(success.todo)
      }
      this.$store.dispatch('success/setSuccessDone', statToUpdate)
    },
    showSuccess(success) {
      const toast = useToast();
      toast.success(`Unlocked success : ${success}`);
    },
    getNewsletterOpenRate(newsletter) {
      if (newsletter.emails_count !== 0 && newsletter.seen_emails_cnt !== 0) {
        let open_rate = newsletter.seen_emails_cnt / newsletter.emails_cnt * 100
        return Math.round(open_rate)
      }
      return 0
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

      let statisticID = 'deleted_emails_newsletters_feature'
      this.updateStatisticsState(statisticID, newsletter.emails_cnt)
      this.updateStatisticsState(['saved_carbon'], newsletter.generated_carbon)

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
    isUnsubscribed(clickedNewsletter) {
      let lastReceptionDate = new Date(this.newsletters[clickedNewsletter].received_at)
      let today = new Date()
      if ((today.getMonth() - lastReceptionDate.getMonth() + (12 * (today.getFullYear() - lastReceptionDate.getFullYear()))) > 3)
        this.newsletters[clickedNewsletter].unsubscribed = true
    },
    //Update the state that keeps the statistics to add the number of deleted emails or unsunscribed newsletters by user.
    updateStatisticsState(statisticID, value) {
      this.$store.dispatch("stats/updateStatistics", {ids: [statisticID], value: value})
          .then(() => {
            // if no success is linked to statisticID then skip it
            if (!this.successDetails[statisticID]) return
            for (const success of this.successDetails[statisticID]) {
              if (this.$store.state.stats.statistics.erasmail[statisticID] >= success.minValue && !success.done)
                this.showSuccess(success.todo)
            }
            this.$store.dispatch('success/setSuccessDone', statisticID)
          })
          .catch((err) => {
            console.log(err)
          })
    },
    unsubscribe(clickedNewsletter) {
      let newsletter = []

      let request_data = {}

      this.newsletters[clickedNewsletter].unsubscribed = true
      this.newsletters[clickedNewsletter].forecasted_carbon = 0

      let statisticID = 'unsubscribed_newsletters'
      this.updateStatisticsState(statisticID, 1)


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

.box {
  min-height: 50%;
}

.box:hover {
  background-color: rgb(247, 245, 245);
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