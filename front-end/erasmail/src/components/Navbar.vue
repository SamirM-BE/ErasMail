<template>
  <nav class="navbar is-light" role="navigation" aria-label="main navigation">
    <!-- LOGO ErasMail -->
    <div class="navbar-brand">
      <router-link class="navbar-item" :to="{ name: 'home' }" exact><strong>ErasMail</strong></router-link>

      <a role="button" class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }"
        aria-label="menu" aria-expanded="false" data-target="navbar">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>

    <!-- Menu -->
    <div id="navbar" class="navbar-menu" :class="{ 'is-active': showNav }">
      <!-- Left side -->
      <div class="navbar-start">
        <router-link v-if="loggedIn" class="navbar-item" :to="{ name: 'threads' }">Threads</router-link> 
         
        <a class="navbar-item is-hidden"> Documentation </a>

        <div class="navbar-item has-dropdown is-hoverable is-hidden">
          <a class="navbar-link"> More </a>

          <div class="navbar-dropdown">
            <a class="navbar-item"> About </a>
            <a class="navbar-item"> Jobs </a>
            <a class="navbar-item"> Contact </a>
            <hr class="navbar-divider" />
            <a class="navbar-item"> Report an issue </a>
          </div>
        </div>
      </div>
      <!-- Right side -->
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <router-link v-if="!loggedIn" class="button is-primary" :to="{ name: 'login' }" exact>Login</router-link>
            <router-link v-else class="button is-danger" :to="{ name: 'logout' }" exact>Logout</router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "Navbar",
  data() {
    return {
      showNav: false,
    };
  },
  computed: mapGetters("auth", ["loggedIn"]),
};
</script>

<style scoped>
</style>

