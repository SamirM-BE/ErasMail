<template>
  <AwarenessMessage :co2="generated_carbon" :forecastCarbon="carbon_yforecast"
                    :forecastMsg="`Keeping these emails for another year will have an additional impact equivalent to `"
                    :itemCount="emailCount"
                    :itemName="featureName"/>
  <div class="toolbox mx-4">
    <hr>
    
    <Dropdown :currentValue="selectedFolder" :defaultText="'Inbox'" :toText="folderToText" :valueList="folderList"
      @on-click="selectFolder" />

    <button class="button is-danger is-pulled-right" :disabled="!checkedEmails.length" @click="remove()">Delete emails</button>

    <div class="mt-2">
      <Dropdown :currentValue="yearBefore" :defaultText="'Any date'" :toText="yearToText" :valueList="yearList"
                @on-click="selectYear"/>
      <Dropdown :currentValue="sizeGreatherThan" :defaultText="'Any size'" :toText="sizeToText" :valueList="sizeList"
                class="mx-3" @on-click="selectSize"></Dropdown>

      <div :class="{'is-active':showFilters}" class="dropdown">
        <div class="dropdown-trigger" @click="showFilters = !showFilters">
          <button aria-controls="dropdown-menu" aria-haspopup="true" class="button">
            <span>Smart filters</span>
            <span class="icon is-small">
              <i aria-hidden="true" class="fas fa-angle-down"></i>
            </span>
          </button>
        </div>
        <div id="dropdown-menu" class="dropdown-menu" role="menu">
          <div class="dropdown-content">
            <form>
              <div v-for="(filterName, idx) in filterNames" :key="idx" class="field dropdown-item">
                <div class="control">
                  <label class="checkbox">
                    <input v-model="selectedFilters" :value="idx" type="checkbox">
                    {{ filterName }}
                  </label>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div class=" button mx-3">
        <label class="checkbox">
          <input v-model="unread" type="checkbox">
          Only unread emails
        </label>
      </div>
      

    </div>
    <hr>
  </div>
  <div class="container">
    <EmailForm :emails="emailList" :reset="reset" class="mx-4" @checked-emails="updateCheckedEmails"/>
  </div>
</template>

<script>
import {getAPI} from "../axios-api";
import AwarenessMessage from "../components/AwarenessMessage";
import EmailForm from "../components/EmailForm";
import Dropdown from "../components/Dropdown";
import {useToast} from "vue-toastification";

export default {
  name: "Emails",
  components: {
    AwarenessMessage,
    EmailForm,
    Dropdown
  },
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
    if (querySelectedFilters) {
      // if only one element is seleted then `querySelectedFilters` is a string type 
      if (typeof (querySelectedFilters) == "string") {
        querySelectedFilters = [querySelectedFilters]
      }
      let allowedFilters = Object.keys(this.filterNames)
      // remove unvalide filters 
      querySelectedFilters = querySelectedFilters.filter(filter => allowedFilters.includes(filter));
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
  mounted() {
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
  computed: {
    featureName() {
      let msg = ''
      if (this.unread) msg += 'unread '
      msg += 'email' + (this.emailCount > 1 ? 's' : '')
      if (this.yearBefore)
        msg += ` older than ${this.yearBefore} year` + (this.yearBefore > 1 ? 's' : '')
      if (this.yearBefore && this.sizeGreatherThan)
        msg += ' and'
      if (this.sizeGreatherThan)
        msg += ` greather than ${this.sizeGreatherThan} MB`
      return msg
    },
    emailList() {
      return Object.values(this.emails)
    },
    // deleted_olderF_count() {
    //   return this.$store.state.stats.deleted_emails_olderF_count
    // },
    // deleted_largerF_count() {
    //   return this.$store.state.stats.deleted_emails_largerF_count
    // },
    // deleted_useless_count() {
    //   return this.$store.state.stats.deleted_emails_useless_count
    // },
    successDetails() {
      return this.$store.state.success.successDetails
    }
  },
  methods: {
    selectFolder(folder) {
      this.selectedFolder = folder
      this.refreshURL()
    },
    folderToText(folder) {
      return folder
    },
    selectYear(year) {
      this.yearBefore = year
      this.refreshURL()
    },
    yearToText(year) {
      let txt = `Older than ${year} year`
      if (year > 1) {
        txt += 's'
      }
      return txt
    },
    selectSize(size) {
      this.sizeGreatherThan = size
      this.refreshURL()
    },
    sizeToText(size) {
      return `Greather than ${size} MB`
    },
    updateCheckedEmails(newCheckedEmails) {
      this.checkedEmails = newCheckedEmails
    },
    fetchNextEmails(newQuery) {
      if (newQuery) {
        this.nextPageNumber = 1
      }
      if (!this.initializationDone || !this.nextPageNumber) {
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
            if (newQuery) {
              this.emails = response.data.results
            } else {
              this.emails.push(...response.data.results)
            }
            if (response.data.next) {
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
      this.reset = !this.reset
      this.fetchNextEmails(true)
    },
    showSuccess(success) {
      const toast = useToast();
      toast.success(`Unlocked success : ${success}`);
    },
    //Get the statistics IDs to update from the setted filters
    getStatsToUpdate() {
      let stats = []
      if (this.yearBefore > 0)
        stats.push('deleted_emails_older_filter')

      if (this.sizeGreatherThan > 0)
        stats.push('deleted_emails_larger_filter')

      if (this.selectedFilters.length > 0)
        stats.push('deleted_emails_useless_filter')
      return stats
    },
    //Update the state that keeps the statistics to add the number of deleted emails by the user with each feature.
    updateStatisticsState(statisticsIDs, value) {
      this.$store
          .dispatch("stats/updateStatistics", {ids: statisticsIDs, value: value})
          .then(() => {
            for (const statisticID of statisticsIDs) {
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

      let statsIDs = this.getStatsToUpdate()
      this.updateStatisticsState(statsIDs, pks.length)

      this.reset = !this.reset
      getAPI
          .delete('/api/emails/', {
            headers: {
              Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
            },
            data: {
              app_password: this.$store.state.auth.app_password,
              host: this.$store.state.auth.host,
              uids: uids,
              pks: pks,
              stats_to_update: this.getStatsToUpdate(),
            }
          })
          .then(() => {
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
#options-button {
  height: 100%;
  border-radius: 15%;
}

#options-button:hover {
  background-color: rgb(247, 245, 245);
}

.toolbox{
  position: -webkit-sticky; /* Safari */
  position: sticky;
  z-index: 2;
  background-color: white;
  top: 3rem;
}


</style>