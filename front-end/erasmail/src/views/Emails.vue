<template>
  <AwarenessMessage :itemCount="emailCount" :itemName="featureName" :co2="co2" />
  <div class="toolbox m-4">
    <div class="is-flex is-justify-content-space-between">
      <div class="is-flex is-align-items-center">
        <span class="dropdown" :class="{'is-active': showDropdownFolder}">
          <div class="dropdown-trigger" @click="showDropdownFolder = !showDropdownFolder">
            <button class="button" aria-haspopup="true" aria-controls="dropdown-folder">
              <span>{{ folderList[selectedFolderIdx] }}</span>
              <span class="icon is-small">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="folders">
            <div class="dropdown-content">
              <a class="dropdown-item" v-for="(folderName, idx) in folderList" :key="idx"
                :class="{'is-active': selectedFolderIdx === idx}" @click="selectFolder(idx)">
                {{folderName}}
              </a>
            </div>
          </div>
        </span>
        <span id="options-button" class="icon is-medium is-clickable" @click="displayOptions()">
          <i class="fas fa-lg  fa-ellipsis-v" />
        </span>
      </div>

      <div>
        <button class="button is-focused is-danger is-light mx-2" @click="remove(true)">Delete attachments</button>
        <button class="button is-focused is-danger" @click="remove(false)">Delete emails</button>
      </div>
    </div>
    <div v-if="showOptions" class="mt-2 is-flex is-align-items-center">
      <div class="dropdown" :class="{'is-active': showDropdownYear}">
        <div class="dropdown-trigger" @click="showDropdownYear = !showDropdownYear">
          <button class="button" aria-haspopup="true" aria-controls="dropdown-years">
            <span v-if="yearBefore==0">Any date</span>
            <span v-else>Older than {{yearBefore}} year<span v-if="yearBefore > 1">s</span></span>
            <span class="icon is-small">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu" role="years">
          <div class="dropdown-content">
            <a class="dropdown-item" v-for="(year, idx) in yearList" :key="idx"
              :class="{'is-active': year === yearBefore}" @click="selectYear(year)">
              <span v-if="year==0">Any date</span>
              <span v-else>Older than {{year}} year<span v-if="year > 1">s</span></span>
            </a>
          </div>
        </div>
      </div>
      <label class="checkbox mx-3">
        <input type="checkbox" v-model="unread">
        Only unread emails
      </label>
    </div>
  </div>
  <hr>
  <div class="emails">
     <EmailForm :emails="emailList" :reset="reset" @checked-emails="updateCheckedEmails" class="mx-4" />
  </div>
</template>

<script>
import {
  getAPI
} from "../axios-api";
import AwarenessMessage from "../components/AwarenessMessage";
import EmailForm from "../components/EmailForm";

export default {
  data() {
    return {
      showOptions: false,

      showDropdownFolder: false,
      folderList: [],
      selectedFolderIdx: 0,

      showDropdownYear: false,
      yearList: [0, 1, 3, 5, 10],
      yearBefore: 0,

      unread: false,

      emails: {},
      checkedEmails: [],

      reset: false,
    }
  },
  created() {
    this.unread = this.$route.query.unseen === 'true'
    let queryYearBefore = parseInt(this.$route.query.before_than)
    if (this.yearList.includes(queryYearBefore)) {
      this.yearBefore = queryYearBefore
    }
    getAPI
      .get(
        "/api/emails/folders", {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
        }
      )
      .then((response) => {
        this.folderList = response.data
        // put the inbox folder at the first position
        let inbox = "inbox"
        this.folderList.sort((x, y) => x.toLowerCase() === inbox ? -1 : y.toLowerCase() == inbox ? 1 : 0)

        this.fetchEmails()
      })
      .catch((err) => {
        console.log(err);
      });
  },
  watch: {
    unread() {
      this.refreshURL()
      this.reset = ! this.reset
    },
    yearBefore() {
      this.refreshURL()
      this.reset = ! this.reset
    },
    selectedFolderIdx(){
      this.fetchEmails()
      this.reset = ! this.reset
    }
  },
  components: {
    AwarenessMessage,
    EmailForm
  },
  computed: {
    featureName() {
      let msg = ''
      if(this.unread) msg += 'unread '
      msg += 'email' + (this.emailCount > 1 ? 's' : '')
      if(this.yearBefore)
         msg += ` older than ${this.yearBefore} year` + (this.yearBefore > 1 ? 's' : '')
      return msg
    },
    emailList(){
      return Object.values(this.emails)
    },
    emailCount() {
      return this.emailList.length
    },
    co2() {
      let pollution = 0.0
      if (this.emailList.length) {
        pollution = this.emailList.map(email => email.co2).reduce((prev, curr) => prev + curr, 0)
      }
      return pollution
    },
  },
  methods: {
    selectFolder(idx) {
      this.showDropdownFolder = false
      this.selectedFolderIdx = idx
    },
    selectYear(year) {
      this.showDropdownYear = false
      this.yearBefore = year
    },
    displayOptions() {
      this.showDropdownFolder = false
      this.showOptions = !this.showOptions
    },
    updateCheckedEmails(newCheckedEmails) {
      this.checkedEmails = newCheckedEmails
    },
    fetchEmails() {
      getAPI
        .get(
          `/api/emails/?seen=${!this.unread}&before_than=${this.yearBefore}&folder=${this.folderList[this.selectedFolderIdx]}`, {
            headers: {
              Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
            },
          }
        )
        .then((response) => {
          this.emails = response.data
        })
        .catch((err) => {
          console.log(err);
        });
    },
    refreshURL() {
      this.$router.replace({
        name: this.$route.name,
        query: {
          unseen: this.unread,
          before_than: this.yearBefore
        }
      })
      this.fetchEmails()
    },
    remove(onlyAttachments) {
      const emailKeys = Object.keys(this.emails)

      let uids = {}
      for (const checkedEmail of this.checkedEmails) {
        let index = emailKeys[checkedEmail]
        let email = this.emails[index]
        // If this email has no attachments so no need to process
        if(onlyAttachments && !email.attachments.length){
          continue
        }
        let selectedUids = uids[email.folder] || []
        selectedUids.push(email.uid)
        uids[email.folder] = selectedUids

        if(onlyAttachments){
          // delete attachments
          let attachmentSize = email.attachments.map(attachment => attachment.size).reduce((prev, curr) => prev + curr, 0)
          email.size = Math.max(0, email.size - attachmentSize)
          email.attachments = []
            //////////////////////
           // TODO update co2 ?//
          //////////////////////
        } else {
          delete this.emails[index]
        }
      }

      this.reset = ! this.reset

      let url = '/api/emails/'
      if (onlyAttachments) {
        url += 'attachments'
      }

      getAPI
        .delete(url, {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
          data: {
            app_password: this.$store.state.auth.app_password,
            host: this.$store.state.auth.host,
            uids: uids
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
}
</script>

<style scoped>
#options-button{
    height: 100%;
    border-radius: 15%;
}
#options-button:hover {
  background-color: rgb(247, 245, 245);
}
.emails{
  overflow-y: scroll;
  height: 63vh;
}


</style>