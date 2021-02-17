<template>
  <div>
      <Navbar></Navbar>
      <div class="hero is-fullheight">
        <div class="hero-body">
          <div class="container">
            <div class="columns is-centered">
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
                    <hr/>
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
                    <label for="application_password" class="label">Application Password</label>
                    <div class="control has-icons-left">
                      <span class="icon is-small is-left">
                        <i class="fa fa-lock"></i>
                      </span>
                      <input id="application_password" class="input" type="text" placeholder="awdlfovxkfxcbbdb" v-model="application_password" />
                    </div>
                  </div>

                  <div class="field">
                    <label for="host" class="label">Host</label>
                    <div class="control">
                      <input id="host" class="input" type="text" placeholder="imap.gmail.com" v-model="host" />
                    </div>
                  </div>

                  <hr />
                  <button class="button is-primary is-fullwidth" :disabled="hideSubmit">
                    Log in
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';

export default {
  name: "Login",
  data() {
    return {
      incorrectAuth: false,
      email: "",
      application_password: "",
      host: "",
    };
  },
  computed: {
    hideSubmit() {
      return this.email == "" || this.application_password == "" || this.host == "";
    },
  },
  components: {
    Navbar,
  },
  methods: {
    login() {
      localStorage.setItem('host', this.host)
      localStorage.setItem('app_password', this.application_password)

      this.$store
        .dispatch("auth/userLogin", {
          email: this.email,
          application_password: this.application_password,
          host: this.host,
        })
        .then(() => {
          this.$router.push({
            name: "loading"
          });
        })
        .catch((err) => {
          console.log(err);
          this.incorrectAuth = true;
        });
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
</style>