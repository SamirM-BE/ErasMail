<template>
    <div class="modal" :class="{ 'is-active': showModal }">
        <div class="modal-background" @click="hideModal()"></div>
        <div class="modal-content">
            <form class="form box" v-on:submit.prevent="login">
                <!---->
                <h1>{{threadSubject}}</h1>
                <div class="box field" v-for="(email, index) in emails" :key="index">
                    <div class="control">
                        <label class="checkbox">
                            <input type="checkbox" :value="index" v-model="checkedEmails">
                            <p> {{email.subject}} {{email.sender_email}} </p>
                            <p> {{email.attachments}} </p>
                        </label>
                    </div>
                </div>
                <!---->
                <div class="field is-grouped">
                    <div class="control">
                        <button class="button is-danger"
                            @click="removeEmails()">Remove</button>
                    </div>
                    <div class="control">
                        <button class="button is-light is-light" @click="hideModal()">Cancel</button>
                    </div>
                    <div>
                        Selected size : {{ selectedSize }}
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
const byteSize = require('byte-size')


export default {
    data() {
        return {
            checkedEmails: []
        }
    },
    computed: {
        selectedSize(){
            let size = 0
            for (let i = 0; i < this.checkedEmails.length; i++) {
                size += this.emails[this.checkedEmails[i]].size
            }
            size = byteSize(size)
            return `${size.value} ${size.unit}`;
        }
    },
    methods: {
        formattedOuput() {
            let output = {}
            for (let i = 0; i < this.checkedEmails.length; i++) {
                //console.log(output)
                let email = this.emails[this.checkedEmails[i]]
                let uids = output[email.folder] || []
                uids.push(email.uid)
                output[email.folder] = uids
            }
            return output
        },
        hideModal(){
            this.checkedEmails = []
            this.$emit('hideModal')
        },
        removeEmails() {
            this.$emit('removeEmails', this.formattedOuput())
            this.hideModal()
        },
    },
    props: ['showModal', 'emails', 'threadSubject'],
    emits: ['hideModal', 'removeEmails'],
}
</script>

<style scoped>
.modal-content {
    max-height: 75%;
    width: 50%;
}
.form {
     height: 100%;
     overflow: auto;
}

.box.field {
    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}


</style>