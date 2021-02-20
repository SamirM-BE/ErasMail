<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
// import axios from 'axios'

export default {
  data() {
    return {
      gap_time: 0,
      beforeUnload_time: 0,
    };
  },
  mounted() {
    window.addEventListener("beforeunload", (e) => this.beforeunloadHandler(e));
    window.addEventListener("unload", (e) => this.unloadHandler(e));
  },
  unmounted() {
    window.removeEventListener("beforeunload", (e) =>
      this.beforeunloadHandler(e)
    );
    window.removeEventListener("unload", (e) => this.unloadHandler(e));
  },
  methods: {
    beforeunloadHandler() {
      this.beforeUnload_time = new Date().getTime();
    },
    unloadHandler() {
      this.gap_time = new Date().getTime() - this.beforeUnload_time;
      if (this.gap_time <= 5) {
        return this.$store.dispatch("auth/userLogout");
      }
    },
  },
};
</script>

<style>
</style>
