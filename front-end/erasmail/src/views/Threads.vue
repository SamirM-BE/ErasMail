<template>
  <article class="message is-link mx-1" v-if="pollutionComparison.comparison">
    <div class="message-body">
      <h3 class="is-size-3 has-text-left">
        You have <strong>{{threadsSorted.length}}</strong> conversation<span
          v-if="threadsSorted.length > 1">s</span>,
        which in turn have already created about
        <strong>{{totalPollution}}g</strong> of CO<sub>2</sub> so far...
      </h3>
      <h4 class="is-size-4 has-text-right is-italic">
        The impact of your conversation<span v-if="threadsSorted.length > 1">s</span> load on the planet is
        about the same as if
        <strong>{{pollutionComparison.comparison.msg}}</strong>
      </h4>
    </div>
  </article>
  <EmailModal :showModal="showModalFlag" :emails="emails" :threadSubject="threadSubject"
              @hide-modal="showModalFlag = false" @remove-emails="removeEmails" @remove-attachments="removeAttachments">
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

// TODO threads = response.data au lieu de response.data.children

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
    totalPollution(){
      // https://www.npmjs.com/package/convert-units
      // do a query to G
      let pollution = 0
      if (this.threads) {
        pollution = this.threads.children.map(thread => thread.co2).reduce((prev, curr) => prev + curr, 0).toFixed(2)
      }
      return pollution
    },
    pollutionComparison(){
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
        //this.threads.children = this.threads.children.filter((thread) => thread.co2 >= 1.4) // 1.4g is the smallest size that can be compared to 1 paper cup
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
    removeAttachments(emails){
      for (let i = 0; i < emails.emailsIndexSize.length ; i++) {
        this.threads.children[this.threadIndex].size -= emails.emailsIndexSize[i].size
        let email = this.threads.children[this.threadIndex].children[emails.emailsIndexSize[i].index]
        email.size -= emails.emailsIndexSize[i].size
        email.attachments = []
      }
      if(emails.uids){
        getAPI
            .delete(
                "/api/emails/attachments", {
                  headers: {
                    Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                  },
                  data: {
                    app_password: this.$store.state.auth.app_password,
                    host: this.$store.state.auth.host,
                    uids:emails.uids
                  }
                }
            )
            .catch((err) => {
              console.log(err);
            });
      }
    },
    removeEmails(emails) {
      // https://vuejs.org/v2/guide/reactivity.html

      if (this.threads.children[this.threadIndex].children.length === emails.emailsIndexSize.length) {
        // if all emails must me removed then remove the whole thread
        this.threads.children.splice(this.threadIndex, 1)
      } else {
        for (let i = emails.emailsIndexSize.length - 1; i >= 0; i--) {
          this.threads.children[this.threadIndex].size -= emails.emailsIndexSize[i].size
          this.threads.children[this.threadIndex].children.splice(emails.emailsIndexSize[i].index, 1)
        }
      }

      getAPI
          .delete(
              "/api/emails/", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
                data: {
                  app_password: this.$store.state.auth.app_password,
                  host: this.$store.state.auth.host,
                  uids:emails.uids
                }
              }
          )
          .catch((err) => {
            console.log(err);
          });
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