<template>
  <div class="columns is-centered is-flex is-align-items-center is-screen-height">
    <div class="column is-one-third">
      <form class="box" v-on:submit.prevent="login">
        <div class="logo has-text-centered">
          <!-- <img src="https://i.imgur.com/vRJbfum.png" width="112" height="28"> -->
          <strong> ErasMail </strong>
        </div>

        <hr/>

        <div v-show="incorrectAuth" class="icon-text has-text-danger has-text-centered">
          <span class="icon">
            <i class="fa fa-exclamation-triangle"></i>
          </span>
          <span>Incorrect email or password !</span>
          <hr />
        </div>

        <div class="field">
          <label for="email" class="label">Email</label>
          <div class="control has-icons-left">
            <span class="icon is-small is-left">
              <i class="fa fa-envelope"></i>
            </span>
            <input id="email" class="input" type="email" placeholder="e.g. alex@example.com" v-model="email" />
          </div>
        </div>

        <div class="field">
          <label for="app_password" class="label">Application Password</label>
          <div class="control has-icons-left">
            <span class="icon is-small is-left">
              <i class="fa fa-lock"></i>
            </span>
            <input id="app_password" class="input" type="text" placeholder="awdlfovxkfxcbbdb" v-model="app_password" />
          </div>
        </div>

        <div class="field" v-if="askForHost">
          <label for="host" class="label">Host</label>
          <div class="control has-icons-left">
            <span class="icon is-small is-left">
              <i class="fas fa-server"></i>
            </span>
            <input id="host" class="input" type="text" placeholder="imap.gmail.com" v-model="host" />
          </div>
        </div>

        <hr />
        <button class="button has-text-white has-background-primary-dark is-fullwidth" :class="{'is-loading': isLookingHost}" :disabled="hideSubmit">
          Log in
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import {fetchConfiguration} from '@/utils/MailConfig.js'

export default {
  name: "Login",
  data() {
    return {
      incorrectAuth: false,
      email: "",
      app_password: "",
      host: "",
      askForHost: false,
      isLookingHost: false,
    };
  },
  computed: {
    hideSubmit() {
      if(this.askForHost)
        return this.email == "" || this.app_password == "" || this.host == "";
      return this.email == "" || this.app_password == ""
    },
  },
  components: {
  },
  methods: {
    login() {
      this.isLookingHost = true
      const that = this
      fetchConfiguration(
          this.email,
          this.app_password,
          function(account){
            that.host = account["imap.host"]
            that.$store
                .dispatch("auth/userLogin", {
                  email: that.email,
                  app_password: that.app_password,
                  host: that.host,
                })
                .then(() => {
                  // redirect only when 200 or 201
                  that.$router.push({
                    name: "loading"
                  });
                })
                .catch((err) => {
                  console.log(err);
                  
                  that.incorrectAuth = true;
                })
                .finally(() =>{
                  that.isLookingHost = false
                });
          },
          function(){
            that.isLookingHost = false
            that.askForHost = true
            console.log("fetch failed")
          }
      )

    },
  },
};
</script>

<style scoped>
.logo {
  padding: 5%;
  border-color: lightgray !important;
  border: solid;
  border-width: thin;
}
.button:hover{
  background-color: hsl(171, 100%, 33%) !important;
}
.is-screen-height {
  min-height: 90vh;
}
</style>