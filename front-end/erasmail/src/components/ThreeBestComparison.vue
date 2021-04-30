<template>
    <section v-show="show && hasComparisons" class="py-2">
        <!-- This is equivalent to: a ameliorer + donner au max les 3 meilleurs comparaison au lieu de tous -->
        <p class="mb-2">{{title}}</p>
        <div class="columns is-centered is-vcentered">
            <div class="column has-text-centered" v-for="(cmp, index) in pollutionWithOr" :key="index">
                <p class="heading is-size-7" v-if="cmp==='or'">or</p>
                <div v-else>
                    <div class="icon">
                        <img :src="require(`../assets/comparisons/${cmp.name}.svg`)"
                            alt="an image showing the comparison of the pollution generated"
                            :title="`This thread pollutes as much as ${cmp.msg}`">
                    </div>
                    <p class="heading">{{cmp.msg}}</p>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import {
    getAllComparisons,
} from "../utils/pollution";
export default {
    props: {
        show: {
            type: Boolean,
            required: true
        },
        title: {
            type: String,
            required: true
        },
        co2: {
            type: Number,
            required: true
        },
    },
    computed: {
        pollutionCmp() {
            let allComparisons = getAllComparisons(this.co2)
            allComparisons.comparisons = allComparisons.comparisons.slice(-3)
            return allComparisons
        },
        pollutionWithOr() {
            return [].concat(...this.pollutionCmp.comparisons.map(n => [n, 'or'])).slice(0, -1)
        },
        hasComparisons() {
            return this.pollutionCmp.comparisons.length
        },
    }
}
</script>

<style scoped>
.heading{
    font-size: 0.55rem;
}
</style>