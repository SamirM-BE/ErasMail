<template>
        <form v-on:submit.prevent="login">
            <div class="field" v-for="(email, index) in emails" :key="index">
                <div class="box control px-0">
                    <input type="checkbox" :value="index" :id="index" v-model="checkedEmails">
                    <label :for="index" class="checkbox is-large">
                        <EmailDetails class="email-details" :email="email" :attachmentStyles="attachmentStyles(index)">
                        </EmailDetails>
                    </label>
                </div>
            </div>
        </form>

</template>

<script>
import EmailDetails from "./EmailDetails";

export default {
    data() {
        return {
            checkedEmails: [],
        }
    },
    props: {
        emails: {
            type: Array,
            required: true
        },
        attachmentStylesList: Array,
        reset: Boolean,
    },
    emits: ['checked-emails'],
    components: {
        EmailDetails,
    },
    watch: {
        reset() {
            this.checkedEmails = []
        },
        checkedEmails() {
            this.$emit('checked-emails', this.checkedEmails)
        },
    },
    methods: {
        attachmentStyles(index){
            if(this.attachmentStylesList){
                return this.attachmentStylesList[index]
            }
            return null
        }
    }
}
</script>

<style scoped>

input {
    margin: 4%;
}

.test {
    background-color: red !important;
}

.email-details {
    border-left-width: thin !important;
    border-left: solid;
    padding-left: 1.5vw;
    height: 100%;
}

.box.control {
    box-shadow: rgba(194, 194, 194, 0.2) 0px 8px 24px;
    display: flex;
    align-items: center;
    justify-content: left;
    /* add a border */
}
</style>