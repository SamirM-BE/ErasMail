<template>
    <article class="message is-link m-4">
        <div class="message-body pb-1">
            <h3 class="is-size-3 has-text-left">
                You have <strong>{{itemCount}}</strong> {{itemName}},
                which have generated about
                <strong>{{ readableCo2 }}</strong> of CO<sub>2</sub> so far...
            </h3>
            <h4 v-if="pollutionComparison.comparison" class="is-size-4 has-text-right is-italic">
                The environmental impact of your conversation<span v-if="itemCount > 1">s</span> on the
                planet is about the same as if <strong>{{pollutionComparison.comparison.msg}}</strong>
            </h4>
            <br>
            <p v-if="forecastPollutionComparison.comparison" class="is-italic">{{ forecastMsg }} {{forecastPollutionComparison.comparison.msg}}</p>
        </div>
    </article>
</template>

<script>
import {getOptimalComparison} from "../utils/pollution";

const convert = require('convert-units');

export default {
    props: {
        itemCount: {
            type: Number,
            required: true
        },
        itemName: {
            type: String,
            required: true
        },
        co2: {
            type: Number,
            required: true
        },
        forecastCarbon: {
            type: Number,
            default: 0
        },
        forecastMsg: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            unread: true,
            yearBefore: 2
        }
    },
    computed: {
        readableCo2() {
            let co2 = convert(this.co2).from('g').toBest({
                exclude: ['mcg', 'mg', 'oz', 'lb', 'mt']
            })
            return `${co2.val.toFixed(2)} ${co2.unit}`
        },
        pollutionComparison() {
            return getOptimalComparison(this.co2)
        },
        forecastPollutionComparison() {
            return getOptimalComparison(this.forecastCarbon)
        }
    }
}
</script>

<style scoped>

</style>