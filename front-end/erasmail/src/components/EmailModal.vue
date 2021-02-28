<template>
    <div class="modal" :class="{ 'is-active': showModal }">
        <div class="modal-background" @click="hideModal()"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <h1>{{threadSubject}}</h1>
            </header>
            <section class="modal-card-body">
                <form class="form" v-on:submit.prevent="login">
                <!---->
                <div class="field" v-for="(email, index) in emails" :key="index">
                    <div class="box control px-0">
                        <input type="checkbox" :value="index" :id="index" v-model="checkedEmails">
                        <label :for="index" class="checkbox is-large">
                            <div class="email-details">
                                <p>{{email.sender_name}} {{email.sender_email}}</p>
                                <p>{{email.subject}}</p>
                                <p>{{readableSize(email.size)}}</p>
                                <p>{{readableDate(email.received_at)}}</p>
                                <p>{{email.attachments}}</p>
                            </div>
                        </label>
                    </div>
                </div>
            </form>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-danger" @click="removeEmails()">Remove</button>
                <button class="button is-light is-light" @click="hideModal()">Cancel</button>
                <div>
                    <progress class="progress is-small is-primary" :value="selectedSize" :max="maxSize"></progress>
                    <p>Selected size : {{readableSize(selectedSize)}} on {{readableSize(maxSize)}}</p>
                </div>
            </footer>
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
    props: ['showModal', 'emails', 'threadSubject'],
    emits: ['hide-modal', 'remove-emails'],
    computed: {
        selectedSize() {
            let size = 0
            for (let i = 0; i < this.checkedEmails.length; i++) {
                size += this.emails[this.checkedEmails[i]].size
            }
            return size;
        },
        maxSize() {
            let size = 0
            for (let i = 0; i < this.emails.length; i++) {
                size += this.emails[i].size
            }
            return size;
        },
    },
    methods: {
        readableSize(size) {
            size = byteSize(size)
            return `${size.value} ${size.unit}`;
        },
        readableDate(date) {
            date = new Date(date)
            return `${(date.getMonth()+1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}/${date.getFullYear().toString().padStart(4, '0')}
                         ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
        },
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
        hideModal() {
            this.checkedEmails = []
            this.$emit('hide-modal')
        },
        removeEmails() {
            this.$emit('remove-emails', this.formattedOuput())
            this.hideModal()
        },
    },
}
</script>

<style scoped>
.modal-card {
    max-height: 90%;
    width: 55%;
}

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