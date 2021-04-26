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
        <router-link v-if="loggedIn" :to="{ name: 'home' }" class="navbar-item">Menu</router-link>
        
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
          <div class="container is-flex is-justify-content-space-around py-1">
            <figure v-for="(badge, idx) in badges" v-bind:key="idx" class="image is-32x32" :class="{'is-lock': badge.savedCarbon > savedCarbon}">
              <img class="is-rounded" :src="require(`../assets/badges/sunflower-36/Sunflower${idx+1}.png`)">
            </figure>
          </div>
        </div>

        <div v-if="loggedIn" class="navbar-item user mr-2">
          <router-link class="icon" :to="{ name: 'user' }" exact>
            <i class="fas fa-user has-text-white"></i>
          </router-link>
        </div>
        
        <div v-if="!loggedIn && currentRouteName !== 'login'" class="navbar-item">
          <router-link :to="{ name: 'login' }" class="button is-primary" exact>Login</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import {mapGetters} from "vuex";
import {badgesData} from "@/gamification-data";
export default {
  name: "Navbar",
  data() {
    return {
      showNav: false,
      badges: badgesData,
    };
  },
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
    currentRouteName() {
      return this.$route.name;
    },
    savedCarbon() {
      return this.$store.state.stats.saved_co2 
    },
  },
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

