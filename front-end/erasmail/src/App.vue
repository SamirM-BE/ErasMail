<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
// import axios from 'axios'

export default {
  mounted() {
    window.addEventListener("unload", (e) => this.unloadHandler(e));
  },
  unmounted() {
    window.removeEventListener("unload", (e) => this.unloadHandler(e));
  },
  methods: {
    //https://github.com/MRtough/blog/blob/70ff937800e13348402c132f1796b79c9193192f/vueBlog/src/App.vue
    unloadHandler() {
        return this.$store.dispatch("auth/userLogout");
    },
  },
}
</script>

<style>
</style>
