<template >
  <div id="app">
    <Navbar v-if="currentRouteName != 'loading'"></Navbar>
      <router-view />
    <Footer></Footer>
  </div>
</template>

<script>
// import axios from 'axios'
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";


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
  components: {
      Navbar,
      Footer,
    },
}
</script>

<style>


/*#app {*/
/*  padding: 50px 0;*/
/*  position: absolute;*/
/*  top: 0;*/
/*  bottom: 0;*/
/*  left: 0;*/
/*  right: 0;*/
/*}*/


</style>
