<template>
  <div class="columns">
    <div class="column sidebar is-narrow is-flex is-flex-direction-column is-justify-content-space-between">
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
      <button class="button is-danger is-fullwidth ml-1 is-bottom" @click="logout()">Logout</button>
    </div>

    <div class="column c1">

      <section class="section user-top">
        <div class="columns is-fullwidth">
          <div class="column is-narrow">
            <div class="columns is-multiline">
              <div class="column is-narrow">
                <figure class="image is-64x64">
                  <img class="is-rounded" src="https://bulma.io/images/placeholders/128x128.png">
                </figure>
              </div>
              <div class="column pb-0">
                <p><strong>Email:</strong></p>
                <p>{{ currentEmail }}</p>
                <p><strong>Nickname:</strong></p>
                <p>{{ currentNickname }}</p>
              </div>
            </div>
            <button v-if="!showSettings" class="button is-text px-0 is-small" @click="showSettings=!showSettings">Change
              nickname
            </button>
            <div v-else class="field is-grouped">
              <p class="control">
                <input v-model="newNickname" class="input" placeholder="New nickname" type="text">
              </p>
              <p class="control">
                <button class="button is-success is-light is-outlined" @click="changeNickname()">
                  Save
                </button>
              </p>
            </div>
          </div>

          <div class="column is-6 has-text-centered">
            <h1 class="title">Congratulations you deleted {{ deletedEmails }} e-mails and saved more than
              {{ readableCo2(savedCarbon) }} of CO<sub>2</sub> !
            </h1>
            <h2 v-if="pollutionComparison.comparison" class="subtitle">This is equivalent to
              <strong>{{ pollutionComparison.comparison.msg }}</strong></h2>
          </div>
        </div>

      </section>
      <!-- BADGES -->
      <section v-if="selectedView == 'Profile'" class="section badges-section">
        <div class="container grid-badges-container has-background-success-light">
          <div v-for="(badge, idx) in badges" v-bind:key="idx" :class="{'is-lock': !badge.done}"
               :title="badge.savedCarbon ? `Save ${readableCo2(badge.savedCarbon)} of CO2`: 'Connect for the first time to ErasMail'">
            <figure class="image p-3 has-background-green-light">
              <img :src="require(`../assets/badges/sunflower-600/Sunflower${idx+1}.png`)">
            </figure>
          </div>
        </div>
        <h4 class="is-size-4 has-text-centered mt-4">
          <div v-if="nextBadgeSavedCarbon">
            Still {{ readableCo2(nextBadgeSavedCarbon - savedCarbon) }} of CO<sub>2</sub> to save to unlock the next
            badge
          </div>
          <div v-else>
            You have unlocked all badges
          </div>
        </h4>
      </section>

      <!-- SUCCESS -->
      <section v-else-if="selectedView == 'Success'" class="section success-section">
        <div class="container success-container has-background-success-light">
          <div v-for="(success, idx) in successList" v-bind:key="idx" :class="{'is-lock': successData[success.id]<success.minValue}"
               :title="success.todo" class="box m-4 p-1 has-background-green-light is-flex is-justify-content-space-between">
            <span class="icon-text is-flex is-align-items-center"> 
              <span :class="{'has-text-bronze': success.difficulty == 1, 'has-text-silver': success.difficulty == 2, 'has-text-gold': success.difficulty == 3}"
                    class="icon is-large">
                <i class="fas fa-lg fa-trophy"></i>
              </span>
              <span>{{ success.todo }}</span>
            </span>      
            <div class="progress-stats mb-1 is-align-self-flex-end">
              <p class="is-size-7 is-pulled-right mr-1">{{Math.min(success.minValue, successData[success.id])}} / {{success.minValue}}</p>
              <progress class="progress is-success is-smaller" :value="Math.min(success.minValue, successData[success.id])" :max="success.minValue"/>
            </div>
          </div>
        </div>
        <h4 class="is-size-4 has-text-centered mt-4">
          Still {{ lockedSuccessCount }} achievements to unlock
        </h4>
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
              <th>CO<sub>2</sub> saved</th>
              <th>Score</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(data, idx) in leaderboardData" v-bind:key="idx" :class="{'is-selected': idx == currentUserIdx}">
              <th>{{ idx + 1 }}</th>
              <td>{{ data.nickname }}</td>
              <td>{{ data.deleted_emails_count }}</td>
              <td>{{ readableCo2(data.saved_co2) }}</td>
              <td>{{ data.score }}</td>
            </tr>
            </tbody>
          </table>
        </div>
        <h4 class="is-size-4 has-text-centered mt-4">
          Remove 2 emails to move up one place in the ranking (TODO)
        </h4>
      </section>
    </div>
  </div>


</template>

<script>
import {getAPI} from "../axios-api";
import {badgesData} from "@/gamification-data";
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

      badges: badgesData,

      currentUserId: 0,
      leaderboardData: [],
      connected_count: 0,
      successData: [],
    }
  },
  created() {
    this.fetchCurrentUser()
    this.fetchUsersStats()
    this.fetchUserStats()
  },
  computed: {
    ...mapGetters("success", ["successList"]),
    currentUserIdx() {
      if (this.leaderboardData.length) {
        return this.leaderboardData.findIndex(data => data.id == this.currentUserId)
      }
      return -1
    },
    savedCarbon() {
      if (this.leaderboardData.length) {
        return this.leaderboardData[this.currentUserIdx].saved_co2
      }
      return 0
    },
    deletedEmails() {
      if (this.leaderboardData.length) {
        return this.leaderboardData[this.currentUserIdx].deleted_emails_count
      }
      return 0
    },
    pollutionComparison() {
      return getOptimalComparison(this.savedCarbon)
    },
    lockedSuccessCount() {
      // return the number of success to unlock
      return this.successList.map(success => this.successData[success.id]<success.minValue).reduce((a, b) => a + b, 0)
    },
    nextBadgeSavedCarbon() {
      for (const badge of this.badges) {
        if (!badge.done) {
          return badge.savedCarbon
        }
      }
      return 0
    }
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

            // update the badges obtained
            for (const badge of this.badges) {
              if (badge.savedCarbon <= this.savedCarbon) {
                badge.done = true
              }
            }
          })
          .catch((err) => {
            console.log(err);
          });
    },
    fetchUserStats()
    {
      getAPI
          .get(
              "/api/emails/stats/user", {
                headers: {
                  Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
                },
              }
          )
          .then((response) => {
            let successData = response.data
            successData['connected_count'] = this.connected_count
            this.successData = successData
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
    }
  }
}
</script>

<style scoped>
.sidebar {
  background: hsl(171, 100%, 22%);
  min-height: 91vh;
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

.is-smaller{
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

.nickname {
  width: 60%;
}

.progress-stats{
  width: 5%;
}

.section .container {
  height: 45vh;
  overflow: auto;
  border-radius: 0.75rem;
}

</style>