<template>
  <div :class="loaderIsActive" class="pageloader"><span class="title">Preparing the page, this will take a few
      seconds</span></div>
  <EmailModal :emails="emails" :showModal="showModalFlag" :threadSubject="threadSubject"
              @delete="deleteEmailsOrAttachments" @hide-modal="showModalFlag = false">
  </EmailModal>
  <AwarenessMessage :co2="totalPollution" :itemCount="threadsSorted.length"
                    :itemName="'conversation' + (threadsSorted.length > 1 ? 's' : '')"/>
  <div :class="{'is-clipped': showModalFlag}" class="columns mx-4 mt-4">
    <div class="column is-half has-border p-0">
      <div class="is-scrollable">
        <ThreadBox v-for="(thread, idx) in threadsSorted" v-bind:key="idx" :co2="thread.generated_carbon"
                   :created_at="new Date(thread.children[0].received_at)"
                   :size="thread.size"
                   :subject="thread.subject" class="thread-box"
                   @click="showModal(thread.subject, thread.children, idx)"></ThreadBox>
      </div>
    </div>
    <div class="column is-half has-border p-0">
      <Treemap :threads_prop="threads"></Treemap>
    </div>
  </div>
</template>

<script>
import {getAPI} from "../axios-api";
import {mapGetters} from "vuex";
import AwarenessMessage from "../components/AwarenessMessage";
import ThreadBox from "../components/ThreadBox";
import Treemap from "../components/Treemap";
import EmailModal from "../components/EmailModal";
import {useToast} from "vue-toastification";


export default {
  name: "Threads",
  components: {
    ThreadBox,
    EmailModal,
    Treemap,
    AwarenessMessage
  },
  data() {
    return {
      threads: {},
      showModalFlag: false,
      threadIndex: -1,
      threadSubject: '',
      emails: [],
      loaderIsActive: 'is-active',
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
        pollution = this.threads.children.map(thread => thread.generated_carbon).reduce((prev, curr) => prev + curr, 0)
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
              for (const success of this.successDetails[statisticID]) {
                if (this.$store.state.stats.statistics[statisticID] >= success.minValue && !success.done)
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
        if (emails.onlyAttachments) {
          url += 'attachments'
        }
        let deleted = false
        if (!emails.onlyAttachments && this.threads.children[this.threadIndex].children.length === emails.count) {
          // if all emails must me deleted then remove the whole thread
          this.threads.children.splice(this.threadIndex, 1)
          deleted = true
        }
        let statisticID = emails.onlyAttachments ? ['deleted_attachments_count'] : ['threads_deleted_emails_count']
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
  height: 70vh;
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