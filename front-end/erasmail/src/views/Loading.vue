<template>
  <SuccessNotification :notificationMessage="'You have successfully logged in!'" :delay="3000" :positionStyle="{top: 0}"/>
  <section class="section erasmail">
    <div class="columns is-centered">
      <div class="column is-4 has-text-centered">
        <strong class="has-text-primary logo"> ErasMail </strong>
      </div>
      <div class="column is-5">
        <div class="content has-text-black">
          <h1><strong>Welcome to <span class="has-text-primary">ErasMail &#127758;</span></strong></h1>
          <p>Erasmail comes with a bunch of tools and features that will help you quickly and efficiently reduce the environmental impact of your mailboxes</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section progress-bar is-flex is-flex-direction-column is-align-items-center mt-5 has-text-black">
    <span class="has-text-weight-bold is-size-3 ">{{waitingText}}</span>
    <p>Analyzing your emails</p>
    <progress class="progress is-small is-primary my-1" max="100"></progress>
    <p>{{ awareness_messages[index] }}</p>
  </section>

  <section class="section mx-6">
    <p class="has-text-centered is-size-4 has-text-black">Explore what you can do</p>
    <br>
    <div class="columns is-centered">
      <div class="column is-one-quarter" v-for="(feature, idx) in featuresToShow" :key="idx">
        <div class="box is-shadowless content py-6">

          <div class="is-size-3 has-text-centered has-text-black">
            <span class="icon is-large is-right">
                <i class="fas fa-sm " v-bind:class="feature.icon"></i>
              </span>
            {{feature.name}}
          </div>
          <br>
          <p class="is-size-5 has-text-justified has-text-weight-light has-text-black">{{feature.content}}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import {getAPI} from "../axios-api";
import {useToast} from "vue-toastification";

import SuccessNotification from "../components/SuccessNotification";

const display_time_awareness = 7; // display time of awareness messages in seconds
const display_time_features = 10; // display time of features in seconds

const awareness_messages = [
  "Compress your files before sending them",
  "Avoid thank-you emails",
  "Deleting 30 emails is equivalent to saving 24 hours of the consumption of a light bulb",
  "Avoid replying to all recipients when not necessary",
  "Download your attachments and delete associated emails whenever possible",
    "Emails are never permanently deleted, they are moved to trash"
];

const features = [{
    name: 'Threads',
    content: "Get a list of your most polluting conversations and delete the related emails or associated attachments",
    icon: "fa-comments",
  },
  {
    name: 'Old Emails',
    content: "Get a list of your oldest emails and delete them",
    icon: "fa-calendar-minus",
  },
  {
    name: 'Large Emails',
    content: "Get a list of your largest emails and delete them",
    icon: "fa-weight-hanging",
  },
  {
    name: 'Unsubscribe',
    content: "See the list of all your subscriptions, unsubscribe or delete the related newsletters emails with one click",
    icon: "fa-unlink",
  },
  {
    name: 'Statistics',
    content: 'Monitor your progress and share it on your social media',
    icon: "fa-chart-pie",
  },
  {
    name: 'Useless',
    content: 'Instantly see a list of your more useless emails based on sophisticated filters',
    icon: "fa-mail-bulk",
  }
]


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function fetchingStatus(task_id, accessToken) {
  let fetchContinue = true
  while (fetchContinue) {
    const response = await getAPI
        .get(`/api/emails/`, {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
              params: {
                task_id: task_id,
              },
            }
        )
    let state = response.data.state === "SUCCESS";
    console.log('state', response.data.state)
    if (state) {
      fetchContinue = false
      return state
    }
    await sleep(10000);
  }
}

export default {
  name: "Loading",
  components: {
    SuccessNotification,
  },
  data() {
    return {
      awareness_counter: Math.floor(Math.random() * awareness_messages.length),
      awareness_messages: awareness_messages,
      features: features,
      feature_counter: 0,
      waitingText: "",
    };
  },
  created() {
    let waitingTime = this.getWaitingTime()
    setInterval(change, 60000);
    this.waitingText = `Estimated waiting time : ${waitingTime} minute(s)`
    let that = this
    function change() {
      if(waitingTime==0) {
        that.waitingText = `Don't worry, depending on the email service provider, analyzing your mailbox could take up to 30 minutes. Estimated waiting time : ${waitingTime} minute(s)`
      }
      else {
        that.waitingText = `Estimated waiting time : ${waitingTime} minute(s)`
        waitingTime--
      }
    }
    getAPI
      .post(
        "/api/emails/", {
          app_password: this.$store.state.auth.app_password,
          host: this.$store.state.auth.host,
        }, {
          headers: {
            Authorization: `Bearer ${this.$store.state.auth.accessToken}`,
          },
        }
      )
      .then((response) => {
        let that = this
        return fetchingStatus(response.data.task_id, that.$store.state.auth.accessToken)
      })
      .then(() => {
        return this.fetchUserStats()
      })
      .then(() => {
        this.$router.push({
          name: "home",
        })
      })
      .catch((err) => {
        console.log(err);
        this.$store.dispatch('auth/userLogout')
          .then(() => {
            this.$router.push({
              name: 'login'
            })
          })
      })
  },
  mounted() {
    setInterval(() => {
      this.awareness_counter++;
    }, 1000 * display_time_awareness);
    setInterval(() => {
      this.feature_counter++;
    }, 1000 * display_time_features);

    document.body.style.backgroundImage = "url('https://i.imgur.com/rfsKDrP.jpg')"
    document.body.style.backgroundSize = "100% auto"
  },
  unmounted() {
    document.body.style.backgroundImage = ""
  },
  computed: {
    index() {
      return this.awareness_counter % this.awareness_messages.length;
    },
    featuresToShow() {
      let i = this.feature_counter % Math.ceil(this.features.length / 3.0);
      let start = i * 3;
      let finish = (i + 1) * 3
      return this.features.slice(start, finish)
    },
    successDetails() {
      return this.$store.state.success.successDetails
    }
  },
  methods: {
    showSuccess(success) {
      const toast = useToast();
      toast.success(`Unlocked success : ${success}`);
    },
    fetchUserStats() {
      return this.$store.dispatch("stats/getInitialState")
          .then(() => {

            //Check if user has unlocked the connected_count success
            let statToUpdate = 'connected_count'
            for (const success of this.successDetails[statToUpdate]) {
              if (this.$store.state.stats.statistics.connected_count === success.minValue) {
                this.showSuccess(success.todo)
              }
            }
            this.$store.dispatch('success/updateAllSuccess',)
          })
    },
    getWaitingTime() {
      let emailsCount = this.$store.state.auth.total
      let emailRate = 0
      if (emailsCount<5000)
        emailRate = 10
      else if (emailsCount<10000)
        emailRate = 15
      else
        emailRate = 20
       // 10emails/second
      let waitingTime = emailsCount/emailRate //seconds
      return Math.ceil(waitingTime/60) //minutes
    },

  },
}
</script>


<style lang="scss" scoped>
$innercolor : rgb(230, 240, 223, 0.9);
$outercolor : rgb(230, 240, 223, 0.7);

.logo {
  font-family: Papyrus;
  font-size: 5rem;
}
.progress {
  width: 30vw;
}
.box{
  height: 100%;
  background: $innercolor;
  background: -webkit-radial-gradient(center, $innercolor, $outercolor);
  background: -moz-radial-gradient(center, $innercolor, $outercolor);
  background: radial-gradient(ellipse at center, $innercolor, $outercolor);
}
</style>