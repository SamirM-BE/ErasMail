<template>
  <div class="box m-1 py-2 px-3 is-clickable" @mouseover="hover = true" @mouseleave="hover = false">
    <section class="is-flex is-justify-content-space-between">
      <div class="subject">
        <strong>{{ subject }}</strong>
      </div>


      <div class="icon-text is-flex is-align-items-center">
        <span class="mx-1">{{readableCo2}} of CO<sub>2</sub></span>
        <div class="icon is-medium has-tooltip-left"
          :class="{'has-tooltip-danger': pollutionLevel > 2, 'has-tooltip-warning': pollutionLevel > 0, 'has-tooltip-success': pollutionLevel == 0}"
          :data-tooltip="pollutionLevel > 2 ?  'This thread has a high pollution':
                         pollutionLevel > 0 ?  'This thread has a mild pollution': 
                                               'This thread has a low pollution'">
          <img :src="require(`../assets/speedometer/speedometer${pollutionLevel}.svg`)"
            alt="an image showing the intensity of the pollution generated">
        </div>
      </div>
    </section>

    <span class="icon-text has-text-link" title="Number of emails from this conversation">
      <span class="icon">
        <i class="fas fa-envelope"></i>
      </span>
      {{emailCount}}
    </span>

    <ThreeBestComparison :show="hover" :co2="co2"
      title="The carbon footprint of this conversation is the same as:" />

    <p v-show="hover && forecast" class="is-italic is-size-7">
      Keeping this conversation for one more additional year will generate as much CO2 as {{forecast}}
    </p>

  </div>
</template>

<script>
import ThreeBestComparison from "./ThreeBestComparison";
import {
    getYearlyCarbonForecast,
    getOptimalComparison
} from "../utils/pollution";
const convert = require('convert-units')


export default {
  data(){
    return {
      hover: false,
    }
  },
  props: {
    subject: {
      type: String,
      required: true
    },
    emailCount: {
      type: Number,
      required: true
    },
    co2: {
      type: Number,
      required: true
    },
    size: {
      type: Number,
      required: true
    },
    created_at: {
      type: Date,
      required: true
    },
  },
  components: {
        ThreeBestComparison,
    },
  computed: {
    readableCo2() {
      let co2 = convert(this.co2).from('g').toBest({ exclude: ['mcg', 'mg', 'oz', 'lb', 'mt'] })
      return `${co2.val.toFixed(2)}${co2.unit}`
    },
    co2Forecast(){
      return getYearlyCarbonForecast(this.created_at, this.size)
    },
    pollutionLevel(){
      return getOptimalComparison(this.co2).level
    },
    forecast(){
      let cmp = getOptimalComparison(this.co2Forecast).comparison
      if(cmp){
        return cmp.msg
      }
      return ''
    }
  },
}
</script>

<style scoped>
@import "./../../node_modules/@creativebulma/bulma-tooltip/dist/bulma-tooltip.min.css";
.subject{
  max-width: 70%;
}
.box {
  min-height: 10%;
  box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}
.box:hover {
  background-color: rgb(247, 245, 245);
}
</style>