<template >
  <div id="app">
    <Navbar v-if="currentRouteName != 'loading'"></Navbar>
    <div id="content">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navbar from "./components/Navbar";

export default {
  components: {
    Navbar,
  },
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
  computed: {
    currentRouteName() {
      return this.$route.name;
    }
  },
  methods: {
    beforeunloadHandler() {
      this.beforeUnload_time = new Date().getTime();
    },
    unloadHandler() {
      this.gap_time = new Date().getTime() - this.beforeUnload_time;
      if (this.gap_time <= 10) {
        return this.$store.dispatch("auth/userLogout");
      }
    },
  },
}
</script>

<style>
/* body{
  background-color: hsl(0, 0%, 96%);
} */

#content{
  /* 3.25rem is the height of the navbar */
  min-height: calc(100vh - 3.25rem);
  /* background-color: greenyellow; */
}
</style>
