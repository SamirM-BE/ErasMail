<template>
  <nav class="navbar is-light" role="navigation" :aria-label="$t('navbar.mainNavigation')">
    <!-- LOGO ErasMail -->
    <div class="navbar-brand">
      <router-link class="navbar-item " :to="{ name: 'home' }" exact><strong>ErasMail</strong></router-link>

      <a role="button" class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }" :aria-label="menu" aria-expanded="false" data-target="navbar">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      </a>
    </div>

    <!-- Menu -->
    <div id="navbar" class="navbar-menu" :class="{ 'is-active': showNav }">
      <!-- Left side -->
      <div class="navbar-start">
        <a class="navbar-item is-hidden">{{ $t('navbar.home') }}</a>

        <a class="navbar-item is-hidden">Documentation </a>

        <div class="navbar-item has-dropdown is-hoverable is-hidden">
          <a class="navbar-link">{{ $t('navbar.more') }}</a>

          <div class="navbar-dropdown">
            <a class="navbar-item">{{ $t('navbar.about') }}</a>
            <a class="navbar-item">{{ $t('navbar.contact') }}</a>
            <hr class="navbar-divider" />
            <a class="navbar-item">{{ $t('navbar.reportAnIssue') }}</a>
          </div>
        </div>
      </div>
      <!-- Right side -->
      <div class="navbar-end">
        <div class="navbar-item">
          <div class="buttons">
            <router-link v-if="!loggedIn" class="button is-primary" :to="{ name: 'login' }" exact>{{ $t('navbar.login') }}</router-link>
            <router-link v-else class="button is-danger" :to="{ name: 'logout' }" exact>{{ $t('navbar.logout') }}</router-link>
            <SwitchLanguage />
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from "vuex";
import SwitchLanguage from '@/components/LanguageSwitcher.vue'

export default {
  name: "Navbar",
  data(){
    return {
      showNav: false
    }
  },
  computed: mapGetters("auth", ["loggedIn"]),
  components : {
    SwitchLanguage
  }
};
</script>

<style scoped>
</style>

