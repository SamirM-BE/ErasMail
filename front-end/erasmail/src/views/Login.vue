<template>
  <div class="columns is-centered">
    <div class="column is-one-third">
      <form class="box" v-on:submit.prevent="login">
        <div class="logo has-text-centered">
          <!-- <img src="https://i.imgur.com/vRJbfum.png" width="112" height="28"> -->
          <strong> ErasMail </strong>
        </div>

        <hr />

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

        <div class="field">
          <label for="host" class="label">Host</label>
          <div class="control has-icons-left">
            <span class="icon is-small is-left">
              <i class="fas fa-server"></i>
            </span>
            <input id="host" class="input" type="text" placeholder="imap.gmail.com" v-model="host" />
          </div>
        </div>

        <hr />
        <button class="button has-text-white has-background-primary-dark is-fullwidth" :disabled="hideSubmit">
          Log in
        </button>
      </form>
    </div>
  </div>
</template>

<script>

export default {
  name: "Login",
  data() {
    return {
      incorrectAuth: false,
      email: "",
      app_password: "",
      host: "",
    };
  },
  computed: {
    hideSubmit() {
      return this.email == "" || this.app_password == "" || this.host == "";
    },
  },
  components: {
  },
  methods: {
    login() {
      this.$store
        .dispatch("auth/userLogin", {
          email: this.email,
          app_password: this.app_password,
          host: this.host,
        })
        .then(() => {
          // redirect only when 200 or 201
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
.button:hover{
  background-color: hsl(171, 100%, 33%) !important;
}
</style>