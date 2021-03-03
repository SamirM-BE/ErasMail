<template>
    <div class="modal" :class="{ 'is-active': showModal }">
        <div class="modal-background" @click="hideModal()"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <h1>{{threadSubject}}</h1>
            </header>
            <section class="modal-card-body p-0 is-clipped">
                <EmailForm :emails="emails" :reset="!showModal" @checked-emails="updateCheckedEmails"></EmailForm>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-danger" @click="removeEmails()">Remove</button>
                <button class="button is-light is-light" @click="hideModal()">Cancel</button>
                <div>
                    <p> Selected size : {{readableSize(selectedSize)}} / {{readableSize(maxSize)}}</p> <!-- / ==> out of -->
                    <progress class="progress is-small is-primary" :value="selectedSize" :max="maxSize"></progress>
                </div>
            </footer>
        </div>
    </div>
</template>

<script>
import EmailForm from "./EmailForm";
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
    components: {
        EmailForm,
    },
    methods: {
        updateCheckedEmails(newCheckedEmails){
            this.checkedEmails = newCheckedEmails
        },
        readableSize(size) {
            size = byteSize(size)
            return `${size.value} ${size.unit}`;
        },
        hideModal() {
            this.checkedEmails = []
            this.$emit('hide-modal')
        },
        removeEmails() {
            let emailsToRemove = {
                emailsIndexSize: [],
                emailsFolderUid: [],
                uids: {}
            }
            for (let i = 0; i < this.checkedEmails.length; i++) {
                let index = this.checkedEmails[i]
                let email = this.emails[index]
                emailsToRemove.emailsIndexSize.push([index, email.size])
                emailsToRemove.emailsFolderUid.push([email.folder, email.uid])

                let uids = emailsToRemove.uids[email.folder] || []
                uids.push(email.uid)
                emailsToRemove.uids[email.folder] = uids
            }
            emailsToRemove.emailsIndexSize.sort((a, b) => a[0] - b[0])
            this.$emit('remove-emails', emailsToRemove)
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

</style>