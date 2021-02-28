<template>
    <form class="form" v-on:submit.prevent="login">
        <div class="field" v-for="(email, index) in emails" :key="index">
            <div class="box control px-0">
                <input type="checkbox" :value="index" :id="index" v-model="checkedEmails">
                <label :for="index" class="checkbox is-large">
                    <EmailDetails class="email-details" :email="email"></EmailDetails>
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
            checkedEmails: []
        }
    },
    props: ['emails', 'reset'],
    emits: ['checked-emails'],
    components: {
        EmailDetails,
    },
    watch: {
        reset(){
            if(this.reset){
                this.checkedEmails = []
            }
        },
        checkedEmails(){
            this.$emit('checked-emails', this.checkedEmails)
        }
    },

}
</script>

<style scoped>

.form {
    height: 100%;
    overflow: auto;
}


input {
    margin: 4%;
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
}
</style>