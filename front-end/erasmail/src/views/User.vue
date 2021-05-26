<template>
  <div class="columns main-layout">
    <div class="column sidebar is-narrow">
      <!--<h1 class="title is-size-5 has-text-white is-uppercase">ErasMail</h1>-->
      <aside class="menu mt-5">
        <ul class="menu-list">
          <li>
            <a :class="{'is-on': selectedView=='Profile'}" class="icon-text has-text-white"
               @click="selectedView = 'Profile'">
              <span class="icon">
                <i class="fas fa-id-badge"></i>
              </span>
              <span>Profile</span>
            </a>
          </li>

          <li>
            <a :class="{'is-on': selectedView=='Success'}" class="icon-text has-text-white"
               @click="selectedView = 'Success'">
              <span class="icon">
                <i class="fas fa-trophy"></i>
              </span>
              <span>Success</span>
            </a>
          </li>

          <li>
            <a :class="{'is-on': selectedView=='Leaderboard'}" class="icon-text has-text-white"
               @click="selectedView = 'Leaderboard'">
              <span class="icon">
                <i class="fas fa-list-ol"></i>
              </span>
              <span>Leaderboard</span>
            </a>
          </li>

          <li>
            <a class="icon-text has-text-white" @click="$router.push({name:'stats'})">
              <span class="icon">
                <i class="fas fa-chart-pie"></i>
              </span>
              <span>Statistics</span>
            </a>
          </li>
        </ul>
      </aside>
    </div>

    <div class="column c1">

      <section class="user-top message is-link m-4">
        <div class="message-body py-3 is-flex is-justify-content-space-between">
          <div class="user-data is-flex-basis-0 is-flex-grow-1">
            <div class="has-text-black">
              <p><strong>Email:</strong> {{ currentEmail }}</p>
              <p><strong>Nickname:</strong> {{ currentNickname }}</p>
            </div>
            <div id="change-nickname">
              <button v-if="!showSettings" class="button is-rounded is-small is-link is-light has-text-link-dark p-0"
                      @click="showSettings=!showSettings">
                <u>Change nickname</u>
              </button>
              <div v-else class="nickname-form mt-1">
                <div class="field">
                  <p class="control">
                    <input v-model="newNickname" class="input is-small" placeholder="New nickname" type="text"
                           @keyup.enter="changeNickname()">
                  </p>
                </div>
                <div class="field is-grouped">
                  <div class="control">
                    <button class="button is-small is-success is-light is-outlined" @click="changeNickname()">
                      Save
                    </button>
                  </div>
                  <div class="control">
                    <button class="button is-small is-danger is-light is-outlined" @click="showSettings=!showSettings">
                      Cancel
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="congratulation has-text-centered">
            <h3 class="is-size-3">Congratulations you deleted {{ deletedEmails }} emails</h3>
            <h3 class="is-size-3"> and saved more than {{ readableCo2(savedCarbon) }} of CO<sub>2</sub> !</h3>
            <h4 v-if="pollutionComparison.comparison" class="is-size-4">This is equivalent to
              <strong>{{ pollutionComparison.comparison.msg }}</strong></h4>
          </div>

          <!-- help to center the congratulation message -->
          <div class="is-flex-basis-0 is-flex-grow-1"/>
        </div>
      </section>


      <!-- BADGES -->
      <section v-if="selectedView == 'Profile'" class="section badges-section">
        <div class="container grid-badges-container has-background-success-light">
          <div v-for="(badge, idx) in badges" v-bind:key="idx" :class="{'is-lock': badge.minValue > savedCarbon}"
               :title="badge.minValue ? `Save ${readableCo2(badge.minValue)} of CO2`: 'Connect for the first time to ErasMail'">
            <figure class="image p-3 has-background-green-light">
              <img :src="require(`../assets/badges/sunflower-600/Sunflower${idx+1}.png`)">
            </figure>
          </div>
        </div>
        <h4 class="is-size-4 has-text-centered mt-4">
          <div v-if="nextBadgeSavedCarbon">
            <p>Save {{ readableCo2(nextBadgeSavedCarbon - savedCarbon) }} of CO<sub>2</sub> to unlock the next badge</p>
            <progress :max="nextBadgeSavedCarbon" :value="savedCarbon"
                      class="progress progress-message is-link is-small"/>
          </div>
          <p v-else>You have unlocked all badges</p>
        </h4>
        <div class="social-sharing is-flex is-justify-content-center">
          <button class="button is-small m-3 is-facebook"
                  @click="openWindowSharing(facebookLink, 'facebook', 'badge')">
                <span class="icon">
                  <i class="fab fa-facebook"></i>
                </span>
            <span>Share on Facebook</span>
          </button>
          <button class="button is-small m-3 is-twitter"
                  @click="openWindowSharing(twitterLink, 'twitter', 'badge')">
                <span class="icon">
                  <i class="fab fa-twitter"></i>
                </span>
            <span>Share on Twitter</span>
          </button>
        </div>
      </section>

      <!-- SUCCESS -->
      <section v-else-if="selectedView == 'Success'" class="section success-section">
        <div class="container success-container has-background-success-light">
          <div v-for="(success, idx) in successList" v-bind:key="idx"
               :class="{'is-lock': successData[success.id]<success.minValue}"
               :title="success.todo"
               class="box m-4 p-1 has-background-green-light is-flex is-justify-content-space-between">
            <span class="icon-text is-flex is-align-items-center"> 
              <span
                  :class="{'has-text-bronze': success.difficulty == 1, 'has-text-silver': success.difficulty == 2, 'has-text-gold': success.difficulty == 3}"
                  class="icon is-large">
                <i class="fas fa-lg fa-trophy"></i>
              </span>
              <span>{{ success.todo }}</span>
            </span>
            <div class="progress-stats mb-1 is-align-self-flex-end">
              <p class="is-size-7 is-pulled-right mr-1">{{ Math.min(success.minValue, successData[success.id]) }} /
                {{ success.minValue }}</p>
              <progress :max="success.minValue"
                        :value="Math.min(success.minValue, successData[success.id])" class="progress is-success is-smaller"/>
            </div>
          </div>
        </div>
        <h4 class="is-size-4 has-text-centered mt-4">
          <p>{{ lockedSuccessCount }} success to unlock</p>
          <progress :max="successList.length" :value="successList.length - lockedSuccessCount"
                    class="progress progress-message is-link is-small"/>
        </h4>
        <div class="social-sharing is-flex is-justify-content-center">
          <button class="button is-small m-3 is-facebook"
                  @click="openWindowSharing(facebookLink, 'facebook', 'success')">
                <span class="icon">
                  <i class="fab fa-facebook"></i>
                </span>
            <span>Share on Facebook</span>
          </button>
          <button class="button is-small m-3 is-twitter"
                  @click="openWindowSharing(twitterLink, 'twitter', 'success')">
                <span class="icon">
                  <i class="fab fa-twitter"></i>
                </span>
            <span>Share on Twitter</span>
          </button>
        </div>
      </section>

      <!-- LEADERBOARD -->
      <section v-else class="section leaderboard-section">
        <div class="container leaderboard-container p-1">
          <table class="table is-bordered is-narrow is-fullwidth">
            <thead>
            <tr>
              <th>Rank</th>
              <th>Nickname</th>
              <th>Deleted emails</th>
              <th>Saved CO<sub>2</sub></th>
              <th>Score</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(data, idx) in leaderboardData" v-bind:key="idx" :class="{'is-selected': idx == currentUserIdx}">
              <th>{{ idx + 1 }}</th>
              <td>{{ data.nickname }}</td>
              <td>{{ data.deleted_emails }}</td>
              <td>{{ readableCo2(data.saved_carbon) }}</td>
              <td>{{ data.score }}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section class="section leaderbord-social">
        <div class="social-sharing is-flex is-justify-content-center">
          <button class="button is-small m-3 is-facebook"
                  @click="openWindowSharing(facebookLink, 'facebook', 'leaderboard')">
                <span class="icon">
                  <i class="fab fa-facebook"></i>
                </span>
            <span>Share on Facebook</span>
          </button>
          <button class="button is-small m-3 is-twitter"
                  @click="openWindowSharing(twitterLink, 'twitter', 'leaderboard')">
                <span class="icon">
                  <i class="fab fa-twitter"></i>
                </span>
            <span>Share on Twitter</span>
          </button>
        </div>
      </section>
    </div>
  </div>


</template>

<script>
import {getAPI} from "../axios-api";
import badgesData from "@/data/badges-data.json";
import {getOptimalComparison} from "../utils/pollution";
import {mapGetters} from "vuex";

const convert = require('convert-units');

export default {
  name: "User",
  data() {
    return {
      selectedView: "Profile",
      showSettings: false,

      currentEmail: "",
      currentNickname: "",
      newNickname: "",

      badges: badgesData.data,

      unlockedBadgesCount: 0,
      unlockedSuccessCount: 0,
      leaderboardRank : 0,

      currentUserId: 0,
      leaderboardData: [],
      connected_count: 0,

      facebookLink: 'https://www.facebook.com/sharer/sharer.php?u=@u&title=@t&description=@d&quote=@q&hashtag=@h',
      twitterLink: 'https://twitter.com/intent/tweet?text=@t&url=@u&hashtags=@h@tu',
    }
  },
  created() {
    this.fetchCurrentUser()
    this.fetchUsersStats()
  },
  computed: {
    ...mapGetters("success", ["successList"]),
    successData() {
      return {...this.$store.state.stats.statistics.erasmail, "connected_count": this.connected_count}
    },
    currentUserIdx() {
      if (this.leaderboardData.length) {
        return this.leaderboardData.findIndex(data => data.id == this.currentUserId)
      }
      return -1
    },
    savedCarbon() {
      let statistics = this.$store.state.stats.statistics
      if (statistics.erasmail) {
        console.log('statistics.erasmail.saved_carbon', statistics.erasmail.saved_carbon)
        return statistics.erasmail.saved_carbon
      }
      return 0
    },
    deletedEmails() {
      if (this.leaderboardData.length) {
        return this.leaderboardData[this.currentUserIdx].deleted_emails
      }
      return 0
    },
    pollutionComparison() {
      return getOptimalComparison(this.savedCarbon)
    },
    lockedSuccessCount() {
      // return the number of success to unlock
      return this.successList.reduce((a, b) => a + (this.successData[b.id] < b.minValue || 0), 0)
    },
    nextBadgeSavedCarbon() {
      for (const badge of this.badges) {
        if (badge.minValue > this.savedCarbon) {
          return badge.minValue
        }
      }
      return 0
    },
  },
  methods: {
    fetchCurrentUser() {
      getAPI
          .get(
              "/api/users/me", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then((response) => {
            this.connected_count = response.data.connected_count
            this.currentEmail = response.data.email
            this.currentNickname = response.data.nickname
          })
          .catch((err) => {
            console.log(err);
          });
    },
    fetchUsersStats() {
      getAPI
          .get(
              "/api/emails/stats/users", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then((response) => {
            this.leaderboardData = response.data.users_stats
            this.currentUserId = response.data.current_user_id
          })
          .catch((err) => {
            console.log(err);
          });
    },
    logout() {
      this.$store.dispatch('auth/userLogout')
          .then(() => {
            this.$router.push({
              name: 'landingpage'
            })
          })
    },
    readableCo2(co2) {
      co2 = convert(co2).from('g').toBest({
        exclude: ['mcg', 'mg', 'oz', 'lb', 'mt']
      })
      return `${Math.round(co2.val)} ${co2.unit}`
    },
    changeNickname() {
      getAPI
          .put(
              "/api/users/me", {
                nickname: this.newNickname,
              }, {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then(() => {
            this.showSettings = !this.showSettings
            // update the user data
            this.currentNickname = this.newNickname
            // update the leaderboard
            this.leaderboardData[this.currentUserIdx].nickname = this.newNickname
            this.newNickname = ""
          })
          .catch((err) => {
            // TODO : si plus grand que 20 char alors erreur le gerer
            console.log(err);
          });
    },
    countUnlockedBadges() {
      let unlockedBadges = 0
      for (const badge of this.badges) {
        if (badge.minValue <= this.savedCarbon) {
          unlockedBadges++
        }
      }
      this.unlockedBadgesCount = unlockedBadges

      this.unlockedSuccessCount = this.successList.length - this.lockedSuccessCount
      this.leaderboardRank = this.currentUserIdx+1

    },
    openWindowSharing(mediaLink, media, gamificationType) {
      this.countUnlockedBadges()
      let promotionalText = ""
      if(gamificationType=="badge"){
        promotionalText =
            `I unlocked ${this.unlockedBadgesCount} badge${this.unlockedBadgesCount>1? 's':''} by saving ${Math.round(this.savedCarbon)}g of CO2 using ErasMail ! \n
            Storing emails has an environmental cost, behind these emails there are servers using electricity. You too can contribute to make the planet a little greener!`
      }
      else if(gamificationType=="success") {
        promotionalText =
            `I unlocked ${this.unlockedBadgesCount} success on ErasMail by cleaning my mailbox ! \n
            Storing emails has an environmental cost, behind these emails there are servers using electricity. You too can contribute to make the planet a little greener!`
      }
      else if(gamificationType=="leaderboard"){
        promotionalText =
            `I'm ${this.leaderboardRank}th in the leaderbord, try to beat me by cleaning your mailbox with ErasMail ! \n
            Storing emails has an environmental cost, behind these emails there are servers using electricity. You too can contribute to make the planet a little greener!`
      }

      //Twitter sharing shouldn't include empty parameter
      if (media === 'twitter') {
        mediaLink = mediaLink.replace('&hashtags=@h', '')
        mediaLink = mediaLink.replace('@tu', '')
      }
      mediaLink = mediaLink.replace(/@tu/g, '&via=' + encodeURIComponent(''))
          .replace(/@u/g, encodeURIComponent('https://www.erasmail.com'))
          .replace(/@q/g, encodeURIComponent(promotionalText))
          .replace(/@d/g, encodeURIComponent(''))
          .replace(/@t/g, encodeURIComponent(promotionalText))
          .replace(/@h/g, '')
          .replace(/@m/g, encodeURIComponent(media))
      window.open(mediaLink, "_blank", `width=${window.screen.width / 2},height=${window.screen.height / 2}`)
    },
  }
}
</script>


<style scoped>
@import "./../../node_modules/bulma-social/css/single/facebook/facebook.min.css";
@import "./../../node_modules/bulma-social/css/single/twitter/twitter.min.css";

.sidebar {
  background: hsl(171, 100%, 22%);
  min-height: calc(100vh - 2.5rem)
}

li a:hover {
  background-color: hsl(171, 100%, 25%);
}

.is-on {
  background-color: hsl(171, 100%, 29%);
}

.is-selected {
  background-color: hsl(171, 100%, 29%) !important;
}

.is-lock {
  opacity: 0.4;
}

.is-smaller {
  height: 0.4rem;
}

.has-text-gold {
  color: gold;
}

.has-text-silver {
  color: silver;
}

.has-text-bronze {
  color: #cd7f32;
}

.has-background-green-light {
  background-color: hsl(142, 52%, 85%);
}

.is-flex-basis-0 {
  flex-basis: 0;
}

.grid-badges-container {
  display: grid;
  width: 100%;
  height: 100%;
  grid-template-columns: repeat(5, 1fr);
  place-items: center;
}

.image {
  width: 6rem;
  border-radius: 0.75rem;
}

.nickname-form .input {
  width: 50%;
}

.nickname {
  width: 60%;
}

.progress-stats {
  width: 5%;
}

.progress-message {
  margin: auto;
  width: 50%;
}

.section .container {
  height: 45vh;
  overflow: auto;
  border-radius: 0.75rem;
}

</style>