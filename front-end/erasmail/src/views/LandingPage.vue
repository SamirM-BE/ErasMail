<template>
  <!-- Promo -->
  <section class="section promo is-medium has-background-success-lighter">
    <div class="columns is-centered">
      <div class="column is-4 promo-left">
        <div class="promo-text">
          <h1 class="title is-1 promo-title">Clean up your inbox</h1>
          <h2 class="subtitle is-3 promo-subtitle">ErasMail is the fastest way to clean up your inbox.</h2>
          <h3 class="subtitle is-4 promo-subtitle">Reduce your digital pollution by deleting multiple emails using the
            various available filters.</h3>
        </div>

        <div class="field is-grouped pt-6 mb-0" v-if="!loggedIn">
          <p class="control has-icons-left has-icons-right">
            <input class="input is-expanded" :class="{'is-danger': !validated}" type="email" placeholder="enter@your.email"
              v-model="email" @keyup.enter="login()">
            <span class="icon is-small  is-left">
              <i class="fas fa-envelope"></i>
            </span>
            <span v-show="!validated" class="icon is-small is-right has-text-danger">
              <i class="fas fa-times"></i>
            </span>
          </p>
          <p class="control">
            <!-- ANALYZE MY MAILBOX -->
            <a class="button is-success" @click="login()">
              Analyze my mailbox
            </a>
          </p>
        </div>
        <p v-show="!validated" class="help is-danger">This email is invalid</p>
      </div>
      <div class="column is-5 promo-right">
        <figure class="image">
          <img src="../assets/erasmail1.png">
        </figure>
      </div>
    </div>
  </section>


  <!--  Rajouter des images-->
  <!-- Awareness -->
  <section class="section awareness has-background-success-light is-medium">
    <div class="container awareness-message">
      <div class="awareness-text has-text-centered">
        <h3 class="subtitle is-3 features-subtitle has-text-weight-semibold">We care about ecology</h3>
        <p class="subtitle is-4 features-explanation mb-0">
          More and more emails are sent every day, those emails end up in data centers that require a lot of energy.
        </p>
        <p class="subtitle is-4 features-explanation">
          The required energy to run data centers is one of the main causes of digital pollution.
        </p>
      </div>
    </div>
  </section>


  <section id="features" class="section is-medium has-background-success-lighter">
    <h1 class="title is-1 promo-title has-text-centered">Features</h1>
    <br>
    <div class="container features-introduction pt-4">
      <div class="columns is-centered test0">
        <div class="column is-9 test1">
          <div class="columns is-centered">
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-unlink"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Unsubscribe</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">See the list of all your subscriptions, unsubscribe or delete the related newsletters emails with one click</h4>
            </div>
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-comments"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Threads</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">Get a list of your most polluting conversations and delete the related emails or associated attachments</h4>
            </div>
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-mail-bulk"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Useless</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">Instantly see a list of your more useless emails based on sophisticated filters</h4>
            </div>
          </div>
          <div class="columns is-centered test2">
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-weight-hanging"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Large</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">Get a list of your largest emails and delete them</h4>
            </div>
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-calendar-minus"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Old</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">Get a list of your oldest emails and delete them</h4>
            </div>
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-chart-pie"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Statistics</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">Obtain detailed statistics on your environmental impact as well as on your use of e-mail services.</h4>
            </div>
          </div>
          <div class="columns is-centered test3">
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-user-lock"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Privacy</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">ErasMail never access the content of your emails, store or sell your data, and do not track you. All metadata from your emails is deleted when you log out. </h4>
            </div>
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-user-shield"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Secure</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">ErasMail do not have access to your e-mail account outside of the browser. All access is made here on your browser using a temporary password </h4>
            </div>
            <div class="column has-text-centered">
              <span class="icon is-large is-right">
                <i class="fas fa-2x fa-trash-alt"></i>
              </span>
              <h3 class="subtitle is-4 features-subtitle m-0">Safe</h3>
              <h4 class="subtitle is-7 features-subtitle has-text-weight-light">Emails are never really deleted, they are moved to the trash folder</h4>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section id="faq" class="section has-background-success-light is-medium">
    <h1 class="title is-1 has-text-centered promo-title">FAQ</h1>
    <br>
    <div class="container">
      <div class="columns">
        <div class="column is-half">
          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">What is the goal of ErasMail?</h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              ErasMail is a service whose sole objective is to reduce the environmental impact of emails. The service is free and open-source.
            </h4>
          </div>

          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">Why do emails pollute?</h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              There is nothing virtual about emails, they are data stored on servers that run on electricity 24 hours a day. This considerable energy need generates a lot of pollution. Deleting your unnecessary emails reduces the size of the data stored on servers and therefore fewer servers are needed.
            </h4>
          </div>

          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">How do you make money?</h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              We do not earn money with ErasMail.
            </h4>
          </div>

          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">Which email providers are supported ? </h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              ErasMail uses IMAP to connect to your mailbox. This allows us to support all providers.
            </h4>
          </div>


        </div>

        <div class="column is-half">
          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">How can I be sure that you don't keep any of my data?</h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              The ErasMail code is open-source, you can found it <a href="https://github.com/SamirM-BE/ErasMail">here</a>.
            </h4>
          </div>

          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">How can I be sure that your service is safe?</h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              To log in we recommend you to generate an application password. It is a temporary password that you can delete after using ErasMail. Application passwords are only generable if you have enabled two-factor authentication.
            </h4>
          </div>

          <div class="box">
            <h3 class="subtitle is-5 has-text-weight-bold mb-0">I'm afraid you might delete some important emails that I would like to keep.</h3>
            <br>
            <h4 class="subtitle is-6 has-text-weight-light">
              ErasMail never automatically delete emails. You always decide which emails to delete. Moreover, emails are not permanently deleted, they are moved to the trash and you make the final decision.
            </h4>
          </div>
        </div>
      </div>
    </div>
  </section>
  <Footer></Footer>
</template>

<script>
import Footer from "../components/Footer";
import {mapGetters} from "vuex";

export default {
  name: "LandingPage",
  computed: {
    ...mapGetters("auth", ["loggedIn"]),
  },
  components: {
    Footer,
  },
  data(){
    return {
      email: '',
      validated: true,
    }
  },
  methods: {
    login(){
      this.validated = this.validEmail(this.email)
      if(this.validated){
        this.$store.dispatch('auth/updateEmail', this.email)
        .then(() => {
          this.$router.push({name: 'login'})
        })
      }
    },
    validEmail(email) {
      let re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return re.test(email)
    }
  },
}
</script>

<style scoped>
Footer {
  width: 100%;
  background-color: hsl(171, 100%, 29%);
}

.box {
  box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

.has-background-success-lighter{
  background-color: hsl(142, 52%, 99%);
}

.has-background-success-light{
  background-color: hsl(142, 52%, 90%)
}

.promo-text {
  font-family: "Calibri Light";
}

.features-explanation {
  font-family: "Garamond";
}


.start {
  width: 30%;
}
</style>