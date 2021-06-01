<template>
  <div :class="loaderIsActive" class="pageloader"><span class="title">Preparing the page, this will take a few
      seconds</span></div>
  <EmailModal :emails="emails" :showModal="showModalFlag" :threadSubject="threadSubject"
              @delete="deleteEmailsOrAttachments" @hide-modal="showModalFlag = false">
  </EmailModal>
  <SuccessNotification :notificationMessage="notificationMessage" :trigger="trigger"/>
  <AwarenessMessage :co2="totalPollution" :itemCount="threadsSorted.length"
                    :itemName="'conversation' + (threadsSorted.length > 1 ? 's' : '')"/>
  <div :class="{'is-clipped': showModalFlag}" class="columns mx-4 mt-4">
    <div class="column is-half has-border p-0">
      <div class="is-scrollable">
        <ThreadBox v-for="(thread, idx) in threadsSorted" v-bind:key="idx" :co2="thread.generated_carbon"
                   :created_at="new Date(thread.children[0].received_at)"
                   :size="thread.size"
                   :subject="thread.subject"
                   :emailCount="thread.children.length"
                   class="thread-box"
                   @click="showModal(thread.subject, thread.children, idx)"></ThreadBox>
      </div>
    </div>
    <!-- need to add is-clipped because some svg inside the Treemap are out of bounds -->
    <div class="column is-half has-border is-clipped p-0">
      <Treemap :threads_prop="threads"></Treemap>
    </div>
  </div>
</template>

<script>
import {getAPI} from "../axios-api";
import {mapGetters} from "vuex";
import {useToast} from "vue-toastification";


import AwarenessMessage from "../components/AwarenessMessage";
import ThreadBox from "../components/ThreadBox";
import Treemap from "../components/Treemap";
import EmailModal from "../components/EmailModal";
import SuccessNotification from "../components/SuccessNotification";


export default {
  name: "Threads",
  components: {
    ThreadBox,
    EmailModal,
    Treemap,
    AwarenessMessage,
    SuccessNotification
  },
  data() {
    return {
      threads: {},
      showModalFlag: false,
      threadIndex: -1,
      threadSubject: '',
      emails: [],
      loaderIsActive: 'is-active',

      trigger: true, // SuccessNotification
      notificationMessage: '', // SuccessNotification
    }
  },
  created() {
    if (this.loggedIn) {
      getAPI
          .get(
              "/api/emails/threads", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then((response) => {
            this.threads = response.data

            //We limit the quantity of threads to show
            //TODO: Should not be done in this way, use pagination instead
            let totalThreads = this.threads.children.length
            if(totalThreads>150){
              this.threads.children = this.threads.children.slice(0,150)
            }
          })
          .catch((err) => {
            console.log(err);
          });
    }
  },
  updated() {
    this.loaderIsActive = ''
  },
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
    threadsSorted() {
      if (this.threads.children) {
        let threadsList = this.threads.children
        threadsList.sort((a, b) => b.generated_carbon - a.generated_carbon)
        return threadsList
      }
      return []
    },
    totalPollution() {
      let pollution = 0.0
      if (this.threads.children) {
        pollution = this.threads.children.reduce((a, b) => a + (b['generated_carbon'] || 0), 0)
      }
      return pollution
    },
    successDetails() {
      return this.$store.state.success.successDetails
    },
  },
  methods: {
    showModal(threadSubject, emails, idx) {
      this.showModalFlag = true
      this.threadSubject = threadSubject
      this.emails = emails
      this.threadIndex = idx
    },
    showSuccess(success) {
      const toast = useToast();
      toast.success(`Unlocked success : ${success}`);
    },
    updateStatisticsState(statisticID, value) {
      this.$store
          .dispatch("stats/updateStatistics", {ids: statisticID, value: value})
          .then(() => {
            for (const statisticID of statisticID) {
              // if no success is linked to statisticID then skip it
              if(!this.successDetails[statisticID]) continue
              for (const success of this.successDetails[statisticID]) {
                if (this.$store.state.stats.statistics.erasmail[statisticID] >= success.minValue && !success.done)
                  this.showSuccess(success.todo)
              }
              this.$store.dispatch('success/setSuccessDone', statisticID)
            }
          })
          .catch((err) => {
            console.log(err)
          })
    },
    deleteEmailsOrAttachments(emails) {
      if (emails.count) {
        let url = '/api/emails/'
        this.notificationMessage = 'Email(s) successfully deleted!'

        if (emails.onlyAttachments) {
          url += 'attachments'
          this.notificationMessage = 'Attachment(s) successfully deleted!'
        }

        let statisticID = emails.onlyAttachments ? ['deleted_attachments'] : ['deleted_emails_threads_feature', 'deleted_emails']
        const carbonYforecast = this.threads.children[this.threadIndex].carbon_yforecast

        let deleted = false
        if (!emails.onlyAttachments && this.threads.children[this.threadIndex].children.length === emails.count) {
          // if all emails must me deleted then remove the whole thread
          this.threads.children.splice(this.threadIndex, 1)
          this.updateStatisticsState(['saved_carbon'], carbonYforecast)
          deleted = true
        }

        this.updateStatisticsState(statisticID, emails.pks.length)

        getAPI
            .delete(url, {
              headers: {
                Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
              },
              data: {
                app_password: this.$store.state.auth.app_password,
                host: this.$store.state.auth.host,
                uids: emails.uids,
                pks: emails.pks,
                stats_to_update: statisticID,
              }
            })
            .then(() => {
              this.trigger = !this.trigger
              if (!deleted) {
                return getAPI
                    .get(
                        `/api/emails/threads/${this.threads.children[this.threadIndex].thread_id}`, {
                          headers: {
                            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                          },
                        }
                    )
              }
            })
            .then((response) => {
              if (response) {
                let threadUpdated = response.data
                this.threads.children[this.threadIndex] = threadUpdated
                this.updateStatisticsState(['saved_carbon'], carbonYforecast - threadUpdated.carbon_yforecast)
              }
            })
      }
    },
  },
}
</script>

<style scoped>
@import "./../../node_modules/bulma-pageloader/dist/css/bulma-pageloader.min.css";

.column {
  height: 75vh;
}

.is-scrollable {
  overflow: auto;
  height: 100%;
}

.has-border {
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}

</style>