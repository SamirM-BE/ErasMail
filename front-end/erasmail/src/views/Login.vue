<template>
  <div class="columns is-centered is-flex is-align-items-center is-screen-height">
    <div class="column is-one-third">
      <div class="box">
        <div class="logo has-text-centered">
          <!-- <img src="https://i.imgur.com/vRJbfum.png" width="112" height="28"> -->
          <strong> ErasMail </strong>
        </div>

        <ul class="steps mt-5">
          <li class="steps-segment" :class="{'is-active': stepIdx === 0}">
            <span class="steps-marker">
              <span class="icon">
                <i class="fas fa-envelope"></i>
              </span>
            </span>
          </li>
          <li class="steps-segment" :class="{'is-active': stepIdx === 1}">
            <span class="steps-marker">
              <span class="icon">
                <i class="fas fa-info"></i>
              </span>
            </span>
          </li>
          <li class="steps-segment" :class="{'is-active': stepIdx === 2}">
            <span class="steps-marker">
              <span class="icon">
                <i class="fas fa-key"></i>
              </span>
            </span>
          </li>
        </ul>
    
        <hr/>

        <div v-show="incorrectAuth" class="icon-text has-text-danger has-text-centered">
          <span class="icon">
            <i class="fa fa-exclamation-triangle"></i>
          </span>
          <span>Incorrect email or password !</span>
          <hr />
        </div>

        <div v-if="stepIdx === 0" class="field">
          <label for="email" class="label">Email</label>
          <div class="control has-icons-left">
            <input id="email" class="input" :class="{'is-danger': !validatedEmail}" type="email" placeholder="e.g. alex@example.com" v-model="email" />
            <span class="icon is-small is-left">
              <i class="fa fa-envelope"></i>
            </span>
          </div>
          <p v-show="!validatedEmail" class="help is-danger">This email is invalid</p>
        </div>

        <div v-else-if="stepIdx === 1">
          <div class="info-box">
            <h5 class="is-size-5"><strong><span class="is-digit">1</span>  Enable two-step verification</strong></h5>
            <p class="is-size-7">The links below will allow you to activate the two-step verification.</p>
            <p class="is-size-7">It is required to generate an application password.</p>
            <br>
            <ul>
              <li>
                <span class="icon-text has-text-grey-darker">
                  <span class="icon">
                    <i class="fab fa-microsoft"></i>
                  </span>
                  <a class="has-text-weight-medium" href="https://account.live.com/proofs/EnableTfa" target="_blank"> Outlook </a>
                </span>
              </li>
              <li>
                <span class="icon-text  has-text-grey-darker">
                  <span class="icon">
                    <i class="fab fa-google"></i>
                  </span>
                  <a class="has-text-weight-medium" href="https://myaccount.google.com/u/1/signinoptions/two-step-verification" target="_blank"> Gmail </a>
                </span>
              </li>
            </ul>
          </div>
          <br>
          <div class="info-box">
            <h5 class="is-size-5"><strong><span class="is-digit">2</span>  Create an application password</strong></h5>
            <p class="is-size-7">Well done, now you have the two-step verification, let's create the application password with the following links:</p>
            <br>
            <ul>
              <li>
                <span class="icon-text  has-text-grey-darker">
                  <span class="icon">
                    <i class="fab fa-microsoft"></i>
                  </span>
                  <a class="has-text-weight-medium" href="https://account.live.com/proofs/AppPassword" target="_blank"> Outlook </a>
                </span>
              </li>
              <li>
                <span class="icon-text  has-text-grey-darker">
                  <span class="icon">
                    <i class="fab fa-google"></i>
                  </span>
                  <a class="has-text-weight-medium" href="https://myaccount.google.com/u/1/apppasswords" target="_blank"> Gmail </a>
                </span>
              </li>
            </ul>
            <br>
            <p class="is-size-7 is-italic has-text-grey-dark">Note: After using ErasMail, it is advised to delete the application password!</p>
          </div>
        </div>

        <div v-else>
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
        </div>

        <br/>

        <div class="columns">
          <div class="column is-half">
            <button v-if="stepIdx !== 0" class="button has-text-white has-background-primary-dark is-fullwidth" 
              @click="stepIdx--">
              Previous
            </button>
          </div>
          
          <div class="column is-half">
            <button class="button has-text-white has-background-primary-dark is-fullwidth" 
              :class="{'is-loading': isLookingHost}" :disabled="hideNext" @click="next()">
              {{ stepIdx === 2 ? "Login" : "Next"}} 
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {fetchConfiguration} from '@/utils/MailConfig.js'
export default {
  name: "Login",
  data() {
    return {
      stepIdx: 0,
      incorrectAuth: false,
      email: this.$store.state.auth.email || "",
      app_password: "",
      host: "",
      askForHost: false,
      isLookingHost: false,
      validatedEmail: true,
    };
  },
  created() {
    if(this.email) {
       this.stepIdx ++
    }
  },
  computed: {
    hideNext() {
      return (this.stepIdx === 0 && this.email == "") ||
             (this.stepIdx === 2 && this.askForHost && (this.app_password == "" || this.host == "")) ||
             (this.stepIdx === 2 && !this.askForHost && this.app_password == "")
    },
  },
  components: {
  },
  methods: {
    validEmail(email) {
      let re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return re.test(email)
    },
    next(){
      if(this.stepIdx === 0 && !this.validEmail(this.email)){
        this.validatedEmail = this.validEmail(this.email)
        return
      }
      if(this.stepIdx === 2){
        this.login()
        return
      }
      this.stepIdx ++
    },
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
                  smtpHost: account["msa.smtp.host"],
                  smtpPort:account["msa.smtp.port"]
                })
                .then(() => {
                  // redirect only when 200 or 201
                  that.$router.push({
                    name: "loading"
                  });
                })
                .catch((err) => {
                  console.log(err);
                  that.stepIdx = 0
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

<style lang="scss" scoped>
$primary-dark: hsl(171, 100%, 29%);
@import "./../../node_modules/bulma-steps-component/bulma/bulma.sass";
$steps-completed-color: $primary-dark;
$steps-active-color: $primary-dark;
@import "./../../node_modules/bulma-steps-component/bulma-steps.sass";

a {
  color: $primary-dark;
}

.is-digit {
  padding: 0 0.4rem;
  border: solid;
  border-width: thin;
  border-radius: 50%;
  border-color: lightgray;
  background-color: $grey-lighter;
  box-shadow: $box-shadow;
}

.logo {
  padding: 5%;
  border: solid;
  border-width: thin;
  border-color: lightgray !important;
}
.button:hover{
  background-color: hsl(171, 100%, 33%) !important;
}
.is-screen-height {
  min-height: 90vh;
}
.info-box{
  background-color: $white-bis;
  padding: $box-padding;
  border: solid;
  border-width: thin;
  border-radius: $box-radius;
  border-color: $white-ter;
}
</style>