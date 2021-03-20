<template>
  <article class="message is-link mx-1">
    <div class="message-body">
      <h3 class="is-size-3 has-text-left">
        You have <strong>{{threadsSorted.length}}</strong> conversation<span
          v-if="threadsSorted.length > 1">s</span>,
        which in turn have already created about
        <strong>{{readableCo2}}</strong> of CO<sub>2</sub> so far...
      </h3>
      <h4 class="is-size-4 has-text-right is-italic" v-if="pollutionComparison.comparison">
        The impact of your conversation<span v-if="threadsSorted.length > 1">s</span> load on the planet is
        about the same as if
        <strong>{{pollutionComparison.comparison.msg}}</strong>
      </h4>
    </div>
  </article>
  <EmailModal :showModal="showModalFlag" :emails="emails" :threadSubject="threadSubject"
              @hide-modal="showModalFlag = false" @delete="deleteEmailsOrAttachments">
  </EmailModal>
  <div class="columns mx-1" :class="{'is-clipped': showModalFlag}">
    <div class="column is-half has-border p-0">
      <div class="is-scrollable">
        <ThreadBox v-for="(thread, idx) in threadsSorted" v-bind:key="idx" :subject="thread.subject"
                   :co2="thread.co2" @click="showModal(thread.subject, thread.children, idx)"></ThreadBox>
      </div>
    </div>
    <div class="column is-half has-border p-0">
      <Treemap :threads_prop="threads"> </Treemap>
    </div>
  </div>
</template>


<script>
import {
  getAPI
} from "../axios-api";
import {
  getOptimalComparison
} from "../utils/pollution";
import {
  mapGetters
} from "vuex";
import ThreadBox from "../components/ThreadBox";
import Treemap from "../components/Treemap";
import EmailModal from "../components/EmailModal";
const convert = require('convert-units');


export default {
  name: "Home",
  data() {
    return {
      threads: null,
      showModalFlag: false,
      threadIndex: -1,
      threadSubject: '',
      emails: [],
    }
  },
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
    threadsSorted() {
      if (this.threads) {
        let threadsList = this.threads.children
        threadsList.sort((a, b) => b.co2 - a.co2)
        return threadsList
      }
      return []
    },
    totalPollution() {
      let pollution = 0.0
      if (this.threads) {
        pollution = this.threads.children.map(thread => thread.co2).reduce((prev, curr) => prev + curr, 0)
      }
      return pollution
    },
    readableCo2() {
      let co2 = convert(this.totalPollution).from('g').toBest({
        exclude: ['mcg', 'mg', 'oz', 'lb', 'mt']
      })
      return `${co2.val.toFixed(2)}${co2.unit}`
    },
    pollutionComparison() {
      return getOptimalComparison(this.totalPollution)
    }
  },
  components: {
    ThreadBox,
    EmailModal,
    Treemap,
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
        ).then((response) => {
          this.threads = response.data
        })
        .catch((err) => {
          console.log(err);
        });
    }
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
        getAPI.delete(
            url, {
              headers: {
                Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
              },
              data: {
                app_password: this.$store.state.auth.app_password,
                host: this.$store.state.auth.host,
                uids: emails.uids
              }
            }
          )
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