<template>
    <div class="modal" :class="{ 'is-active': showModal }">
        <div class="modal-background" @click="hideModal()"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <h1>{{threadSubject}}</h1>
            </header>
            <section class="modal-card-body p-0">
                <div class="duplicate-message has-background-danger-light has-text-danger-dark has-text-centered"
                    v-if="numberOfDuplicate != 0">
                    <p v-if="numberOfDuplicate==1"> There is {{numberOfDuplicate}} potential duplicate attachment</p>
                    <p v-else> There are {{numberOfDuplicate}} potential duplicate attachments</p>
                </div>
                <EmailForm :class="{'mt-4': numberOfDuplicate != 0}" :emails="emails" :attachmentStylesList="attachmentStyles" :reset="!showModal" @checked-emails="updateCheckedEmails"></EmailForm>
            </section>
            <footer class="modal-card-foot">
                <button class="button is-danger" @click="removeEmails()">Remove</button>
                <button class="button is-light is-light" @click="hideModal()">Cancel</button>
                <div>
                    <p> Selected size : {{readableSize(selectedSize)}} / {{readableSize(maxSize)}}</p>
                    <!-- / ==> out of -->
                    <progress class="progress is-small is-primary" :value="selectedSize" :max="maxSize"></progress>
                </div>
            </footer>
        </div>
    </div>
</template>

<script>
import EmailForm from "./EmailForm";
import {
    UnionFind
} from "../utils/UnionFind";
const byteSize = require('byte-size')
const stringSimilarity = require("string-similarity");
const randomColor = require('random-color');

export default {
    data() {
        return {
            checkedEmails: []
        }
    },
    props: {
        showModal: {
            type: Boolean,
            required: true
        },
        emails: {
            type: Array,
            required: true
        },
        threadSubject: {
            type: String,
            required: true
        },
        
    },
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
        attachments() {
            let attachments = []
            for (let i = 0; i < this.emails.length; i++) {
                attachments.push(...this.emails[i].attachments)
            }
            return attachments
        },
        clusterOfAttachments() {
            let uf = new UnionFind(this.attachments.length)
            for (let i = 0; i < this.attachments.length; i++) {
                for (let j = 0; j < this.attachments.length; j++) {

                    if (this.attachments[i].name.includes(this.attachments[j].name) ||
                        stringSimilarity.compareTwoStrings(this.attachments[i].name, this.attachments[j].name) >= 0.8) {
                        uf.union({
                            idx: i,
                            name: this.attachments[i].name
                        }, {
                            idx: j,
                            name: this.attachments[j].name
                        })

                    }
                }
            }
            return uf
        },
        attachmentStyles() {
            let attachmentStyles = []
            for (let i = 0; i < this.emails.length; i++) {
                let styles = []
                for (let j = 0; j < this.emails[i].attachments.length; j++) {
                    let name = this.emails[i].attachments[j].name
                    if (this.clusterOfAttachments.numberOfMembre(name) > 1) {
                        styles.push(this.colors[this.clusterOfAttachments.groupNumber(name) % this.colors.length])
                    } else {
                        styles.push(null)
                    }
                }
                attachmentStyles.push(styles)
            }
            return attachmentStyles
        },
        numberOfDuplicate() {
            let clusters = new Set()
            for (let i = 0; i < this.attachments.length; i++) {
                let name = this.attachments[i].name
                if (this.clusterOfAttachments.numberOfMembre(name) > 1) {
                    clusters.add(this.clusterOfAttachments.groupNumber(name))
                }
            }
            return clusters.size
        },
        colors() {
            let colors = []
            for(let i = 0; i < this.attachments.length; i++){
                colors.push(randomColor(0.99,0.95).hexString())
            }
            return colors
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

.duplicate-message {
    position: absolute;
    width: 100%;
    z-index: 1;
}


</style>