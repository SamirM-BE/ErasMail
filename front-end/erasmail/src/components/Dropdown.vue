<template>
    <div class="dropdown is-fullwidth" :class="{'is-active': showDropdown}">
        <div class="dropdown-trigger is-fullwidth" @click="showDropdown = !showDropdown">
            <button class="button is-fullwidth has-background-success-light is-flex is-justify-content-space-between" aria-haspopup="true"
                aria-controls="dropdown">
                <span v-if="currentValue==defaultValue">{{defaultText}}</span>
                <span v-else>{{toText(currentValue)}}</span>
                <span class="icon is-small">
                    <i class="fas fa-angle-down" aria-hidden="true"></i>
                </span>
            </button>
        </div>
        <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
                <a class="dropdown-item" v-for="(value, idx) in valueList" :key="idx"
                    :class="{'is-active': value === currentValue}" @click="onClick(value)">
                    <span v-if="value==defaultValue">{{defaultText}}</span>
                    <span v-else>{{toText(value)}}</span>
                </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        defaultText: {
            type: String,
            default: 'Any'
        },
        toText: {
            type: Function,
            default: x => x, // by defaut the identity function 
        },
        defaultValue: {
            type: [String, Number],
            default: 0
        },
        currentValue:{
            type: [String, Number],
            required: true
        },
        valueList:{
            type: Array,
            required: true
        },
        reset:{
            type: Boolean,
            default: false
        },
    },
    emits: ['on-click'],
    data() {
        return {
            showDropdown: false,
        }
    },
    watch:{
        reset(){
            this.showDropdown = false
        }
    },
    methods:{
        onClick(value){
            this.showDropdown = false
            this.$emit('on-click', value)
        }
    } 
}
</script>

<style scoped>
.is-fullwidth{
    width: 100%;
}
</style>