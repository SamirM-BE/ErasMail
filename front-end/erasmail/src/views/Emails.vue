<template>
  <AwarenessMessage :itemCount="emailCount" :itemName="featureName" :co2="generated_carbon"
    :forecastCarbon="carbon_yforecast"
    :forecastMsg="`Keeping these emails for another year will have an additional impact equivalent to `" />
  <div class="toolbox m-4">
    <div class="is-flex is-justify-content-space-between">
      <Dropdown :defaultText="'Inbox'" :toText="folderToText" :currentValue="selectedFolder" :valueList="folderList"
          @on-click="selectFolder" />

      <button class="button is-focused is-danger" @click="remove()">Delete emails</button>
    </div>
    <div class="mt-2 is-flex is-align-items-center">
      <Dropdown :defaultText="'Any date'" :toText="yearToText" :currentValue="yearBefore" :valueList="yearList"
        @on-click="selectYear" />
      <Dropdown class="mx-3" :defaultText="'Any size'" :toText="sizeToText" :currentValue="sizeGreatherThan"
        :valueList="sizeList" @on-click="selectSize"></Dropdown>

      <div class="dropdown" :class="{'is-active':showFilters}">
        <div class="dropdown-trigger" @click="showFilters = !showFilters">
          <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
            <span>Smart filters</span>
            <span class="icon is-small">
              <i class="fas fa-angle-down" aria-hidden="true"></i>
            </span>
          </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu" role="menu">
          <div class="dropdown-content">
            <form>
              <div class="field dropdown-item" v-for="(filterName, idx) in filterNames" :key="idx">
                <div class="control">
                  <label class="checkbox">
                    <input type="checkbox" :value="idx" v-model="selectedFilters">
                    {{ filterName }}
                  </label>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>

      <label class="checkbox mx-3">
        <input type="checkbox" v-model="unread">
        Only unread emails
      </label>

    </div>
    <hr>
  </div>
  <div class="container">
    <EmailForm :emails="emailList" :reset="reset" @checked-emails="updateCheckedEmails" class="mx-4" />
  </div>
</template>

<script>
import {
  getAPI
} from "../axios-api";
import AwarenessMessage from "../components/AwarenessMessage";
import EmailForm from "../components/EmailForm";
import Dropdown from "../components/Dropdown";

export default {
  data() {
    return {
      showDropdownFolder: false,
      folderList: [],
      selectedFolder: 'Inbox',

      yearList: [0, 1, 3, 5, 10],
      yearBefore: 0,
  
      sizeList: [0, 1, 2, 5], // in MB
      sizeGreatherThan: 0,

      unread: false,

      showFilters: false,
      selectedFilters: [],
      filterNames: {
        reminder: 'Reminder',
        welcome: 'Welcome',
        invitation: 'Invitation',
        meeting: 'Meeting',
        verification: 'Verification',
        update: 'Update',
        confirmation: 'Confirmation',
        social: 'Social',
        no_reply: 'No reply',
      },

      nextPageNumber: 1,

      emailCount: 0,
      generated_carbon: 0,
      carbon_yforecast: 0,
      emails: [],
      checkedEmails: [],

      reset: false,
      
      initializationDone: false, // to check if all variables used for the backend request are correctly initialized or not
    }
  },
  created() {
    this.unread = this.$route.query.unseen === 'true'
    
    let queryYearBefore = parseInt(this.$route.query.before_than)
    if (this.yearList.includes(queryYearBefore)) {
      this.yearBefore = queryYearBefore
    }
    let querySizeGreatherThan = parseInt(this.$route.query.greater_than)
    if (this.sizeList.includes(querySizeGreatherThan)) {
      this.sizeGreatherThan = querySizeGreatherThan
    }

    let querySelectedFilters = this.$route.query['selected_filters[]']
    if(querySelectedFilters){
      // if only one element is seleted then `querySelectedFilters` is a string type 
      if(typeof(querySelectedFilters) == "string"){
        querySelectedFilters = [querySelectedFilters]
      }
      let allowedFilters = Object.keys(this.filterNames)
      // remove unvalide filters 
      querySelectedFilters =  querySelectedFilters.filter(filter => allowedFilters.includes(filter));
      this.selectedFilters = querySelectedFilters
    }

    this.initializationDone = true

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
      })
      .catch((err) => {
        console.log(err);
      });

    this.refreshURL()
  },
  mounted () {
    window.onscroll = () => {
      let bottomOfWindow = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop) + window.innerHeight === document.documentElement.offsetHeight
      if (bottomOfWindow) {
        this.fetchNextEmails(false)
      }
    }
  },
  watch: {
    unread() {
      this.refreshURL()
    },
    selectedFilters() {
      this.refreshURL()
    },
  },
  components: {
    AwarenessMessage,
    EmailForm,
    Dropdown
  },
  computed: {
    featureName() {
      let msg = ''
      if(this.unread) msg += 'unread '
      msg += 'email' + (this.emailCount > 1 ? 's' : '')
      if(this.yearBefore)
         msg += ` older than ${this.yearBefore} year` + (this.yearBefore > 1 ? 's' : '')
      if(this.yearBefore && this.sizeGreatherThan)
         msg +=  ' and'
      if(this.sizeGreatherThan)
         msg += ` greather than ${this.sizeGreatherThan} MB`
      return msg
    },
    emailList(){
      return Object.values(this.emails)
    },
  },
  methods: {
    selectFolder(folder) {
      this.selectedFolder = folder
      this.refreshURL()
    },
    folderToText(folder){
      return folder
    },
    selectYear(year) {
      this.yearBefore = year
      this.refreshURL()
    },
    yearToText(year){
      let txt =  `Older than ${year} year`
      if(year > 1){
        txt += 's'
      }
      return txt
    },
    selectSize(size) {
      this.sizeGreatherThan = size
      this.refreshURL()
    },
    sizeToText(size){
      return `Greather than ${size} MB`
    },
    updateCheckedEmails(newCheckedEmails) {
      this.checkedEmails = newCheckedEmails
    },
    fetchNextEmails(newQuery) {
      if(newQuery) {
        this.nextPageNumber = 1
      }
      if(!this.initializationDone || !this.nextPageNumber){
        // if the variables used for the backend request are not correctly initialized or if there is no page to retrieve.
        // thus don't query the backend
        return
      }
      getAPI
      .get(
        `/api/emails/`, {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
          params: {
            seen: !this.unread,
            selected_filters: this.selectedFilters,
            before_than: this.yearBefore,
            greater_than: this.sizeGreatherThan,
            folder: this.selectedFolder,
            page: this.nextPageNumber,
          }
        }
      )
      .then((response) => {
        console.log(response.data)
        this.emailCount = response.data.count
        this.generated_carbon = response.data.generated_carbon
        this.carbon_yforecast = response.data.carbon_yforecast
        if(newQuery){
          this.emails = response.data.results
        } else {
          this.emails.push(...response.data.results)
        }
        if(response.data.next){
          this.nextPageNumber = new URL(response.data.next).searchParams.get('page')
        } else {
          this.nextPageNumber = null
        }
      })
      .catch((err) => {
        console.log(err);
      })
    },
    refreshURL() {
      this.$router.replace({
        name: this.$route.name,
        query: {
          unseen: this.unread,
          before_than: this.yearBefore,
          greater_than: this.sizeGreatherThan,
          'selected_filters[]': this.selectedFilters,
        }
      })
      this.reset = ! this.reset
      this.fetchNextEmails(true)
    },
    remove() {
      const emailKeys = Object.keys(this.emails)

      let uids = {}
      let pks = []
      for (const checkedEmail of this.checkedEmails) {
        let index = emailKeys[checkedEmail]
        let email = this.emails[index]

        pks.push(email.id)
        
        let selectedUids = uids[email.folder] || []
        selectedUids.push(email.uid)
        uids[email.folder] = selectedUids

        delete this.emails[index]
      }

      this.reset = ! this.reset

      getAPI
        .delete('/api/emails/', {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
          data: {
            app_password: this.$store.state.auth.app_password,
            host: this.$store.state.auth.host,
            uids: uids,
            pks: pks
          }
        })
        .then(()=>{
          this.fetchNextEmails(true)
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

</style>