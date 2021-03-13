<template>
  <section class="section cmp p-0">
    <div class="columns">
      <div class="pricing-table">
        <div class="column c1">
          <div class="pricing-plan current is-success">
            <div class="plan-header">Current situation</div>
            <div class="title is-4 has-text-centered has-text-success">
              You saved 900g CO<sub>2</sub>. This is the same as if your drove 5
              km in an average car.
            </div>
            <div class="plan-items">
              <div class="plan-item has-background-primary-light">
                900 g CO<sub>2</sub> saved
              </div>
              <div class="plan-item has-background-primary-light">
                365 deleted emails
              </div>
            </div>
            <div class="plan-footer">
              <button class="button is-fullwidth">Share</button>
            </div>
          </div>
        </div>
        <div class="column c2">
          <apexchart
              :options="radialBar"
              :series="radialBar.series"
              type="radialBar"
              width="100%"
          ></apexchart>
        </div>
        <div class="column c3">
          <div class="pricing-plan potential is-warning">
            <div class="plan-header">Potential impact</div>
            <div class="title is-4 has-text-centered has-text-warning-dark">
              You are wasting 5 kg CO<sub>2</sub> on potentially unnecessary
              emails. This is the same as if your drove 75 km in an average car.
            </div>
            <div class="plan-items">
              <div class="plan-item has-background-warning-light">
                2.3 kg CO<sub>2</sub> potentially savable
              </div>
              <div class="plan-item has-background-warning-light">
                3841 potentially unnecessary emails
              </div>
            </div>
            <div class="plan-footer">
              <button class="button is-fullwidth">Take action</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section stats">
    <div class="tile is-ancestor">
      <div class="tile is-vertical is-8">
        <div class="tile">
          <div class="tile is-parent is-vertical">
            <article class="tile is-child notification is-warning">
              <p class="title">On average you open 30% of your e-mails.</p>
              <p class="subtitle">This is equivalent to ...</p>
            </article>
            <article class="tile is-child notification is-danger">
              <p class="title">Your e-mail box uses 5GB.</p>
              <p class="subtitle">
                It's equivalent to 2 Paris-New York plane travels
              </p>
            </article>
          </div>
          <div class="tile is-parent is-vertical">
            <article class="tile is-child notification is-light">
              <p class="title">E-mail box size evolution</p>
              <p class="subtitle">With an image</p>
              <!-- <figure class="image is-4by3"> -->
              <apexchart
                  :options="chartOptions"
                  :series="series"
                  type="line"
                  width="100%"
              ></apexchart>
              <!-- </figure> -->
            </article>
          </div>
        </div>
        <div class="tile">
          <div class="tile is-parent">
            <article class="tile is-child notification is-link is-light">
              <p class="title">You receive on average 321 e-mails a month</p>
              <p class="subtitle">This is equivalent to ....</p>
              <div class="content">
                This is 21% more than the average users
              </div>
            </article>
          </div>
          <div class="tile is-parent">
            <article class="tile is-child notification is-danger is-light ">
              <p class="title">You have 3256 unread e-mails.</p>
              <p class="subtitle">
                It's equivalent to 2 Paris-New York plane travels
              </p>
              <div class="content">
                This is 17% less than the average users
              </div>
            </article>
          </div>
        </div>
      </div>
      <div class="tile is-parent is-vertical">
        <article class="tile is-child notification is-warning is-light">
          <div class="content">
            <p class="title">You are subscribed to 53 newsletters</p>
            <p class="subtitle">You might receive 5263 e-mail this year.</p>
            <div class="content">
              <!-- Content -->
            </div>
          </div>
        </article>
        <article class="tile is-child notification is-primary is-light">
          <div class="content">
            <p class="title">You unsubscribed from 12 newsletters</p>
            <p class="subtitle">You avoided 1254 e-mails.</p>
            <div class="content">
              <!-- Content -->
            </div>
          </div>
        </article>
        <article class="tile is-child notification is-success">
          <div class="content">
            <p class="title">You pollute 36% less than the average user.</p>
            <p class="subtitle">Pas d'inspi.</p>
            <div class="content">
              <!-- Content -->
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script>
// import MonthlyChart  from "../components/LineChart.vue";
import VueApexCharts from "vue3-apexcharts";

export default {
  name: "Stats",
  data() {
    return {
      radialBar: {
        chart: {
          height: 280,
          type: "radialBar",
        },
        series: [44, 55, 67],
        colors: ["hsl(141, 71%, 48%)"],
        plotOptions: {
          radialBar: {
            track: {
              background: "hsl(48, 100%, 67%)",
              opacity: 0.4,
            },

            // hollow: {
            // 	margin: 15,
            // 	size: "70%"
            // },
            dataLabels: {
              name: {
                fontSize: "22px",
              },
              value: {
                fontSize: "16px",
              },
              total: {
                show: true,
                label: "Currently saved",
                formatter: function (w) {
                  return (
                      (
                          w.globals.seriesTotals.reduce((a, b) => {
                            return a + b;
                          }, 0) / w.globals.series.length
                      ).toPrecision(2) + "% / Total potential"
                  );
                },
              },
            },
          },
        },
        // stroke: {
        // 	lineCap: "round",
        // },
        labels: ["Newsletters", "E-mails", "CO2"],
      },
      chartOptions: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          categories: ["Before ErasMail", "13/03/2021"],
        },
      },
      series: [
        {
          name: "series-1",
          data: [6, 4],
        },
      ],
    };
  },
  components: {
    // MonthlyChart,
    apexchart: VueApexCharts,
  },
  methods: {},
  created() {
  },
};
</script>

<style scoped>
@import "./../../node_modules/bulma-pricingtable/dist/css/bulma-pricingtable.min.css";

.potential,
.current {
  height: 95%;
}

/* .cmp {
    padding: 10px;
    border: 1px solid hsl(141, 71%, 48%);
    box-shadow:  -1px 1px hsl(141, 71%, 48%),
         -2px 2px hsl(141, 71%, 48%),
         -3px 3px hsl(141, 71%, 48%),
         -4px 4px hsl(141, 71%, 48%),
         -5px 5px hsl(141, 71%, 48%);  
} */

.cmp {
  -webkit-box-shadow: 3px 3px 5px 6px #ccc; /* Safari 3-4, iOS 4.0.2 - 4.2, Android 2.3+ */
  -moz-box-shadow: 3px 3px 5px 6px #ccc; /* Firefox 3.5 - 3.6 */
  box-shadow: 3px 3px 5px 6px #ccc; /* Opera 10.5, IE 9, Firefox 4+, Chrome 6+, iOS 5 */
}

/* .p1  {
  width: 30%;
}

.p2  {
  width: 60%;
} */
</style>
