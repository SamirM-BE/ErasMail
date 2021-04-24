<template>
    <form>
        <div class="field" v-for="(email, index) in emails" :key="index">
            <div class="box control px-0 py-1">
                <input type="checkbox" class="m-5" :value="index" :id="index" v-model="checkedEmails">
                <label :for="index" class="checkbox">
                    <EmailDetails class="has-border-left" :email="email" :attachmentStyles="attachmentStylesList[index]">
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
        selectAll: {
            type: Boolean,
            default: false
        },
        attachmentStylesList: {
            type: Array,
            default: () => [],
        },
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
        selectAll(newValue) {
            if (newValue) {
                this.checkedEmails = Array.from({
                    length: this.emails.length
                }, (_, index) => index);
            } else {
                this.checkedEmails = []
            }
        }
    },
}
</script>

<style scoped>
label {
    width: 100%;
}

.has-border-left {
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
    border-color: lightgray !important;
    border: solid;
    border-width: thin;
}
</style>