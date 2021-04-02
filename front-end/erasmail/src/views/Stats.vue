<template>
  <section class="section cmp">
    <div class="columns">
      <div class="pricing-table">

        <div class="column c1">
          <div class="pricing-plan current is-success">
            <div class="plan-header">Current impact</div>
            <div class="title is-4 has-text-centered has-text-success">
              You saved {{ Math.round(userStats.saved_co2) }} CO<sub>2</sub>.
            </div>
            <div class="subtitle is-5 is-italic has-text-centered has-text-success">
              {{ getCO2equivalent(userStats.saved_co2) }}
            </div>
            <div class="plan-items">
              <div class="plan-item has-background-success-light">
                {{ Math.round(userStats.saved_co2) }}g CO<sub>2</sub> saved
              </div>
              <div class="plan-item has-background-success-light">
                {{ userStats.deleted_emails_count }} deleted emails
              </div>
            </div>
            <div class="plan-footer">
              <button class="button is-small m-3 is-facebook has-background-facebook"
                      @click="openWindowSharing(facebookLink, 'facebook')">
                <span class="icon">
                  <i class="fab fa-facebook"></i>
                </span>
                <span>Share on Facebook</span>
              </button>
              <button class="button is-small m-3 is-twitter has-background-twitter"
                      @click="openWindowSharing(twitterLink, 'twitter')">
                <span class="icon">
                  <i class="fab fa-twitter"></i>
                </span>
                <span>Share on Twitter</span>
              </button>
            </div>
          </div>
        </div>

        <div class="column c2">
          <apexchart
              :options="radialBarPotentialImpact"
              :series="radialBarPotentialImpact.series"

              type="radialBar"

          ></apexchart>
        </div>

        <div class="column c3">
          <div class="pricing-plan potential is-warning">
            <div class="plan-header">Potential impact</div>
            <div class="title is-4 has-text-centered has-text-warning-dark">
              You're wasting XXXX kg of CO<sub>2</sub> on emails you probably won't open.
            </div>
            <div class="subtitle is-5 is-italic has-text-centered has-text-warning-dark">
              This is the same as if your drove XXXX km in an average car.
            </div>
            <div class="plan-items">
              <div class="plan-item has-background-warning-light">
                XXXX kg CO<sub>2</sub> potentially savable
              </div>
              <div class="plan-item has-background-warning-light">
                XXXX potentially unnecessary emails
              </div>
            </div>
            <div class="plan-footer">
              <router-link :to="{ name: 'home' }" class="button is-fullwidth">Take action</router-link>
            </div>
          </div>
        </div>

      </div>
    </div>

  </section>

  <section class="section stats">
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-8">
        <div class="tile">
          <div class="tile is-parent is-vertical">
            <article class="tile is-child notification is-warning">
              <p class="title">On average you open
                {{ getUserOpenRate() }}% of your
                emails.</p>
              <div class="content">
                This is {{ getStrEcoComparison(getUserOpenRate(), erasmailStats.avg_open_rate * 100) }} than the average
                user.
              </div>
            </article>
            <article class="tile is-child notification is-danger">
              <p class="title">Your email box uses {{ getStrMailboxSize() }}</p>
              <p class="subtitle">
                {{ getCO2equivalent(userStats.carbon_eq) }}
              </p>
              <div class="content">
                This is {{ getStrEcoComparison(userStats.mailbox_size, erasmailStats.avg_mailbox_size) }} than the
                average user.
              </div>
            </article>
          </div>
          <div class="tile is-parent is-vertical">
            <article class="tile is-child notification is-light">
              <p class="title">Saved CO<sub>2</sub> grams evolution</p>
              <apexchart
                  :options="lineSizeMailbox.chartOptions"
                  :series="lineSizeMailbox.series"
                  type="area"
                  width="100%"
              ></apexchart>
            </article>
          </div>
        </div>
        <div class="tile">
          <div class="tile is-parent">
            <article class="tile is-child notification is-link is-light">
              <p class="title">You receive on average
                {{ getAvgMonthlyEmails() }}
                emails a month</p>
              <p class="subtitle is-7">This statistic is based on the undeleted emails that are currently in your
                mailbox.</p>
              <div class="content">
                This is {{ getStrEcoComparison(getAvgMonthlyEmails(), erasmailStats.avg_monthly_emails_received) }} than
                the average user.
              </div>
            </article>
          </div>
          <div class="tile is-parent">
            <article class="tile is-child notification is-danger is-light ">
              <p class="title">You have {{ userStats.emails_count - userStats.emails_seen_count }} unread emails.</p>
              <p class="subtitle">
                {{ getCO2equivalent(userStats.emails_unseen_co2) }}
              </p>
            </article>
          </div>
        </div>
      </div>
      <div class="tile is-parent is-vertical">
        <article class="tile is-child notification is-warning is-light">
          <div class="content">
            <p class="title">You are subscribed to {{ userStats.newsletters_count }} newsletters</p>
            <p class="subtitle">You might receive {{ Math.round(userStats.newsletters_subscribed_email_yearly_sum) }} emails this year.</p>
            <div class="content">
              <!-- Content -->
            </div>
          </div>
        </article>
        <article class="tile is-child notification is-primary is-light">
          <div class="content">
            <p class="title">You unsubscribed from {{ userStats.unsubscribed_newsletters_count }} newsletters</p>
            <p class="subtitle">You avoided {{ Math.round(userStats.newsletters_unsubscribed_email_yearly_sum) }} emails.</p>
            <div class="content">
              <!-- Content -->
            </div>
          </div>
        </article>
        <article class="tile is-child notification is-success">
          <div class="content">
            <p class="title">You pollute
              {{ getStrEcoComparison(userStats.carbon_eq, erasmailStats.avg_carbon_eq) }}
              than the average user.</p>
            <div class="content">
              <!-- Content -->
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script>
import VueApexCharts from "vue3-apexcharts";
import {lineSizeMailbox, radialBarPotentialImpact} from "@/apex-data";
import {getAPI} from "@/axios-api";
import {mapGetters} from "vuex";
import byteSize from "byte-size"
import axios from 'axios'
import {getOptimalComparison} from '../utils/pollution'

export default {
  name: "Stats",
  data() {
    return {
      radialBarPotentialImpact: radialBarPotentialImpact,
      lineSizeMailbox: lineSizeMailbox,
      userStats: {},
      erasmailStats: {},
      facebookLink: 'https://www.facebook.com/sharer/sharer.php?u=@u&title=@t&description=@d&quote=@q&hashtag=@h',
      twitterLink: 'https://twitter.com/intent/tweet?text=@t&url=@u&hashtags=@h@tu',
    };
  },
  created() {
    this.fetchStats()
  },
  computed: mapGetters(["auth"]),
  components: {
    apexchart: VueApexCharts,
  },
  methods: {
    fetchStats() {
      const resquestUserStats = getAPI.get(
          "/api/emails/stats/user", {
            headers: {
              Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
            },
          }
      )
      const requestErasmailStats = getAPI.get(
          "/api/emails/stats/erasmail", {
            headers: {
              Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
            },
          }
      )
      axios.all([resquestUserStats, requestErasmailStats])
          .then((responses) => {
            this.userStats = responses[0].data
            console.log(responses[0].data)
            this.erasmailStats = responses[1].data
            this.updateDataRadialbar()
          })
          .catch((err) => {
            console.log(err);
          });
    },
    updateDataRadialbar() {
      //Newsletters
      let newslettersUnsubPercent = 0
      if (this.userStats.newsletters_count !== 0 && newslettersUnsubPercent !== 0) {
        newslettersUnsubPercent = (this.userStats.unsubscribed_newsletters_count / this.userStats.newsletters_count).toPrecision(2) * 100
        radialBarPotentialImpact.labels.push("Newsletters")
        radialBarPotentialImpact.series.push(newslettersUnsubPercent)
      }

      //Emails
      radialBarPotentialImpact.labels.push("E-mails")
      radialBarPotentialImpact.series.push(44)

      //CO2
      radialBarPotentialImpact.labels.push("CO2")
      radialBarPotentialImpact.series.push(55)
    },
    openWindowSharing(mediaLink, media) {

      //Twitter sharing shouldn't include empty parameter
      if (media === 'twitter') {
        mediaLink = mediaLink.replace('&hashtags=@h', '')
        mediaLink = mediaLink.replace('@tu', '')
      }
      mediaLink = mediaLink.replace(/@tu/g, '&via=' + encodeURIComponent(''))
          .replace(/@u/g, encodeURIComponent('https://www.erasmail.com'))
          .replace(/@t/g, encodeURIComponent(`Storing emails has an environmental cost, behind these emails there are servers using electricity.\nI deleted ${this.userStats.deleted_emails_count} emails and saved ${Math.round(this.userStats.saved_co2)}g of CO2 thanks to ErasMail. You too can contribute to make the planet a little greener!`))
          .replace(/@d/g, encodeURIComponent(''))
          .replace(/@q/g, encodeURIComponent(`Storing emails has an environmental cost, behind these emails there are servers using electricity.\nI deleted ${this.userStats.deleted_emails_count} emails and saved ${Math.round(this.userStats.saved_co2)}g of CO2 thanks to ErasMail. You too can contribute to make the planet a little greener!`))
          .replace(/@h/g, '')
          .replace(/@m/g, encodeURIComponent(media))
      window.open(mediaLink, "_blank", `width=${window.screen.width / 2},height=${window.screen.height / 2}`)
    },
    getUserOpenRate() {
      if (this.userStats.emails_count !== 0)
        return Math.round((this.userStats.emails_seen_count / this.userStats.emails_count) * 100)
      return 0
    },
    getStrMailboxSize() {
      const size = byteSize(this.userStats.mailbox_size)
      return `${size.value} ${size.unit}`
    },
    getAvgMonthlyEmails() {
      if (this.userStats.months_since_creation !== 0)
        return Math.round(this.userStats.emails_count / this.userStats.months_since_creation)
      return 0
    },
    getStrEcoComparison(currentPerformance, avgPerformance) {
      if (avgPerformance !== 0) {
        const performance = Math.round(((currentPerformance - avgPerformance) / avgPerformance) * 100)
        if (performance > 0)
          return `${performance}% more`
        return `${Math.abs(performance)}% less`
      }
      return 0
    },
    getCO2equivalent(carbon) {
      let equivalent = getOptimalComparison(carbon)
      if (equivalent.comparison)
        return `It's equivalent to ${equivalent.comparison.msg}.`
      return ""
    }


  }
};
</script>

<style scoped>
@import "./../../node_modules/bulma-pricingtable/dist/css/bulma-pricingtable.min.css";
@import "./../../node_modules/bulma-social/css/single/facebook/facebook.min.css";
@import "./../../node_modules/bulma-social/css/single/twitter/twitter.min.css";
@import "./../../node_modules/bulma-social/css/single/linkedin/linkedin.min.css";


.potential,
.current {
  height: 95%;
}

.cmp {
  -webkit-box-shadow: 3px 3px 5px 6px #ccc; /* Safari 3-4, iOS 4.0.2 - 4.2, Android 2.3+ */
  -moz-box-shadow: 3px 3px 5px 6px #ccc; /* Firefox 3.5 - 3.6 */
  box-shadow: 3px 3px 5px 6px #ccc; /* Opera 10.5, IE 9, Firefox 4+, Chrome 6+, iOS 5 */
}

</style>
