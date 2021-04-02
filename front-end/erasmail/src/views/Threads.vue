<template>
  <div :class="loaderIsActive" class="pageloader"><span class="title">Preparing the page, this will take a few
      seconds</span></div>
  <EmailModal :showModal="showModalFlag" :emails="emails" :threadSubject="threadSubject"
    @hide-modal="showModalFlag = false" @delete="deleteEmailsOrAttachments">
  </EmailModal>
  <AwarenessMessage :itemCount="threadsSorted.length" :co2="totalPollution"
    :itemName="'conversation' + (threadsSorted.length > 1 ? 's' : '')" />
  <div class="columns mx-4 mt-4" :class="{'is-clipped': showModalFlag}">
    <div class="column is-half has-border p-0">
      <div class="is-scrollable">
        <ThreadBox class="thread-box" v-for="(thread, idx) in threadsSorted" v-bind:key="idx" :subject="thread.subject" :co2="thread.generated_carbon"
          :size="thread.size" :created_at="new Date(thread.children[0].received_at)"
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



export default {
  name: "Home",
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
  },
  components: {
    ThreadBox,
    EmailModal,
    Treemap,
    AwarenessMessage
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
  methods: {
    showModal(threadSubject, emails, idx) {
      this.showModalFlag = true
      this.threadSubject = threadSubject
      this.emails = emails
      this.threadIndex = idx
    },
    deleteEmailsOrAttachments(emails) {
      // https://vuejs.org/v2/guide/reactivity.html
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