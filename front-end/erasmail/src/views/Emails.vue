<template>
  <AwarenessMessage :co2="generated_carbon" :forecastCarbon="carbon_yforecast"
                    :forecastMsg="`Keeping these emails for one more additional year will generate as much CO2 as `"
                    :itemCount="emailCount"
                    :itemName="featureName"/> <!-- manufacturing of 1 more paper cup(s) -->

  <div class="container">
    <div class="columns">
      <!-- Filters -->
      <div class="column is-2 filters">
        <div class="filter-item">
          <p><strong>Folder:</strong></p>
          <Dropdown :currentValue="selectedFolder" :defaultText="'Inbox'" :toText="folderToText" :valueList="folderList"
            @on-click="selectFolder" />
        </div>

        <div class="filter-item mt-3">
          <p><strong>Older than:</strong></p>
          <Dropdown :currentValue="yearBefore" :defaultText="'Any date'" :toText="yearToText" :valueList="yearList"
            @on-click="selectYear"/>
        </div>

        <div class="filter-item mt-3">
          <p><strong>Greater than:</strong></p>
          <Dropdown :currentValue="sizeGreaterThan" :defaultText="'Any size'" :toText="sizeToText" :valueList="sizeList"
            @on-click="selectSize"></Dropdown>
        </div>

        <hr class="my-3">

        <div class="filter-item button is-fullwidth has-background-success-light">
          <label class="checkbox">
            <input v-model="unread" type="checkbox">
            Only unread emails
          </label>
        </div>

        <hr class="my-3">

        <div class="filter-item">
          <p><strong>Useless emails:</strong></p>
          <form class="mt-2">
            <div v-for="(filterName, idx) in filterNames" :key="idx" class="field">
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

      <!-- Emails -->
      <div class="column">
        <div class="toolbox mx-2">
          <hr class="mb-1">
          <div class="is-flex is-justify-content-space-between">
            <div>
              <p><strong>Order by:</strong></p>
              <Dropdown :currentValue="orderedBy" :valueList="Object.keys(orderFilters)" :toText="key => orderFilters[key]"
                @on-click="selectOrder"></Dropdown>
            </div>

            <button class="button is-danger is-align-self-flex-end" :disabled="!checkedEmails.length" @click="deleteEmails()">Delete emails</button>
          </div>
          <hr class="mt-2">
        </div>

        <!-- List of emails -->
        <EmailForm class="mx-2" :emails="emailList" :reset="reset" @checked-emails="updateCheckedEmails" />
      </div>
    </div>
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
      sizeGreaterThan: 0,

      orderedBy: '-received_at',
      orderFilters: {
        '-received_at':'Date recent to old',
        'received_at':'Date old to recent',
        '-size':'Size descending',
        'size':'Size ascending',
        '-generated_carbon':'Generated carbon descending',
        'generated_carbon':'Generated carbon ascending',
        '-carbon_yforecast':'Carbon forecast descending',
        'carbon_yforecast':'Carbon forecast ascending',
      },

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
      ready: true, // whether ready to fetch new data from the backend
    }
  },
  created() {
    this.unread = this.$route.query.unseen === 'true'

    let queryOrderedBy = this.$route.query.ordered_by
    if (Object.keys(this.orderFilters).includes(queryOrderedBy)) {
      this.orderedBy = queryOrderedBy
    }

    let queryYearBefore = parseInt(this.$route.query.before_than)
    if (this.yearList.includes(queryYearBefore)) {
      this.yearBefore = queryYearBefore
    }
    let querysizeGreaterThan = parseInt(this.$route.query.greater_than)
    if (this.sizeList.includes(querysizeGreaterThan)) {
      this.sizeGreaterThan = querysizeGreaterThan
    }

    let querySelectedFilters = this.$route.query['selected_filters[]']
    if (querySelectedFilters) {
      // if only one element is seleted then `querySelectedFilters` is a string type 
      if (typeof (querySelectedFilters) == "string") {
        querySelectedFilters = [querySelectedFilters]
      }
      let allowedFilters = Object.keys(this.filterNames)
      // delete unvalide filters 
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
      let bottomOfWindow = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop) + window.innerHeight >= Math.round(document.documentElement.offsetHeight * 0.95)
      if (bottomOfWindow && this.ready) {
        this.ready = false
        let response = this.fetchNextEmails(false)
        if (response) {
          response.then(() => {
            this.ready = true
          })
        }
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
      if (this.yearBefore && this.sizeGreaterThan)
        msg += ' and'
      if (this.sizeGreaterThan)
        msg += ` greater than ${this.sizeGreaterThan} MB`
      return msg
    },
    emailList() {
      return Object.values(this.emails)
    },
    successDetails() {
      return this.$store.state.success.successDetails
    }
  },
  methods: {
    selectOrder(order) {
      this.orderedBy = order
      this.refreshURL()
    },
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
      let txt = `${year} year`
      if (year > 1) {
        txt += 's'
      }
      return txt
    },
    selectSize(size) {
      this.sizeGreaterThan = size
      this.refreshURL()
    },
    sizeToText(size) {
      return `${size} MB`
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
      return getAPI
          .get(
              `/api/emails/`, {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
                params: {
                  seen: !this.unread,
                  selected_filters: this.selectedFilters,
                  before_than: this.yearBefore,
                  greater_than: this.sizeGreaterThan,
                  folder: this.selectedFolder,
                  page: this.nextPageNumber,
                  ordered_by: this.orderedBy,
                }
              }
          )
          .then((response) => {
            if(response.data.next) console.log('next page number (first page is 1)', new URL(response.data.next).searchParams.get('page'))
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
          greater_than: this.sizeGreaterThan,
          ordered_by: this.orderedBy,
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

      if (this.sizeGreaterThan > 0)
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
    deleteEmails() {
      const emailKeys = Object.keys(this.emails)

      let uids = {}
      let pks = []
      let savedCarbon = 0
      for (const checkedEmail of this.checkedEmails) {
        let index = emailKeys[checkedEmail]
        let email = this.emails[index]

        pks.push(email.id)
        savedCarbon += email.generated_carbon

        let selectedUids = uids[email.folder] || []
        selectedUids.push(email.uid)
        uids[email.folder] = selectedUids

        delete this.emails[index]
      }

      let statsIDs = this.getStatsToUpdate()
      this.updateStatisticsState(statsIDs, pks.length)
      this.updateStatisticsState(['saved_carbon'], savedCarbon)

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
.toolbox{
  position: -webkit-sticky; /* Safari */
  position: sticky;
  z-index: 2;
  top: 3.25rem;
  background-color: rgb(255, 255, 255);
}

</style>