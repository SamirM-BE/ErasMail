<template>
  <nav aria-label="main navigation" class="navbar is-primary has-background-primary-dark is-fixed-top"
       role="navigation">
    <!-- LOGO ErasMail -->
    <div class="navbar-brand">
      <router-link :to="{ name: 'landingpage' }" class="navbar-item" exact><strong>ErasMail</strong></router-link>
      <a :class="{ 'is-active': showNav }" aria-expanded="false" aria-label="menu" class="navbar-burger"
         data-target="navbar" role="button" @click="showNav = !showNav">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <!-- Menu -->
    <div id="navbar" class="navbar-menu" :class="{ 'is-active': showNav }">
      <!-- Left side -->
      <div class="navbar-start">
        <router-link v-if="loggedIn && currentRouteName !== 'home'  && currentRouteName !== 'login'" :to="{ name: 'home' }" class="navbar-item">Menu</router-link>
        
        <div class="navbar-item has-dropdown is-hoverable is-hidden">
          <a class="navbar-link"> More </a>

          <div class="navbar-dropdown">
            <a class="navbar-item"> About </a>
            <a class="navbar-item"> Jobs </a>
            <a class="navbar-item"> Contact </a>
            <hr class="navbar-divider"/>
            <a class="navbar-item"> Report an issue </a>
          </div>
        </div>

      </div>
      <!-- Right side -->
      <div class="navbar-end">

        <div v-if="loggedIn" class="navbar-item badges">
          <div class="container is-flex is-justify-content-space-around py-1 is-clickable" @click="$router.push({name: 'user', query: {view: 'badges'}})">
            <div v-for="(badge, idx) in badges" :key="idx" :class="{'is-lock': badge.minValue > savedCarbon}"
              :title="badge.minValue ? `Save ${readableCo2(badge.minValue)} of CO2`: 'Connect for the first time to ErasMail'">
              <figure class="image is-32x32">
                <img class="is-rounded" :src="require(`../assets/badges/sunflower-36/Sunflower${idx+1}.png`)">
              </figure>
            </div>
          </div>
        </div>

        <div v-if="loggedIn" class="navbar-item user">
          <span class="icon is-clickable" @click="$router.push({name: 'user'})">
            <i class="fas fa-user has-text-white"></i>
          </span>
        </div>

        
        <div class="navbar-item">
          <!-- <router-link v-if="!loggedIn && currentRouteName !== 'login'" :to="{ name: 'login' }" class="button is-primary" exact>Login</router-link> -->
          <button v-if="loggedIn" class="button is-danger"  @click="logout()">Logout</button>
        </div>
        
      </div>
    </div>
  </nav>
</template>

<script>
import {mapGetters} from "vuex";
import badgesData from "@/data/badges-data.json";

const convert = require('convert-units');

export default {
  name: "Navbar",
  data() {
    return {
      showNav: false,
      badges: badgesData.data,
    };
  },
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
    currentRouteName() {
      return this.$route.name;
    },
    savedCarbon() {
      let statistics = this.$store.state.stats.statistics
      if(statistics.erasmail) {
        return statistics.erasmail.saved_carbon
      }
      return 0
    },
  },
  methods: {
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
  }
}
</script>

<style scoped>
.badges {
  width: 100%;
}

.navbar-end {
  width: 25%;
}

.navbar-brand .navbar-item:hover{
  background-color: hsl(171, 100%, 25%) !important;
}

.navbar-start .navbar-item:hover{
  background-color: hsl(171, 100%, 25%) !important;
}

.is-lock {
  opacity: 0.4;
}
/*Tentative 1*/

.image {
  background-color: hsl(171, 100%, 29%);
  border-radius: 0.75rem;
  padding: 3px;  /* changer px */
}

.container {
  background-color: hsl(171, 100%, 22%);
  border-radius: 0.75rem;
}


/*Tentative 2:*/
/*.image {*/
/*  box-shadow: 2px -1px 5px hsl(0, 0%, 29%);*/
/*  border-radius: 50% 50% 50% 50% / 12% 12% 88% 88%;*/
/*  background-color: hsl(171, 100%, 41%);*/
/*}*/


</style>

