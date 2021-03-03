<template>
    <form v-on:submit.prevent="login">
        <div class="field" v-for="(email, index) in emails" :key="index">
            <div class="box control px-0">
                <input type="checkbox" :value="index" :id="index" v-model="checkedEmails">
                <label :for="index" class="checkbox is-large">
                    <!-- faire passer une list de attachments-styles  
                        for eamil in email
                            si pas attachment alors push -1 
                            si attachment alors push [ x, x, x ] une valeur par attachment et -1 si pas ducplicate
                    -->
                    <!-- faire passer une list de couleur
                            index = numberOfGroup
                    -->
                    <!--
                        idéé mettre directement les couleur dans  attachments-styles
                    -->
                    <EmailDetails class="email-details" :email="email" :attachmentStyles="attachmentStyles[index]"></EmailDetails>
                </label>
            </div>
        </div>
    </form>
</template>

<script>
import EmailDetails from "./EmailDetails";
import {UnionFind} from "../utils/UnionFind";
const stringSimilarity = require("string-similarity");
const colors = ['red', 'green', 'blue', 'orange', 'yellow']; // add more colors

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
            this.checkedEmails = []
        },
        checkedEmails(){
            this.$emit('checked-emails', this.checkedEmails)
        }
    },
    computed: {
        attachments(){
            let attachments = []
            for(let i = 0; i < this.emails.length; i++){
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
                        uf.union({idx:i, name:this.attachments[i].name}, {idx:j, name:this.attachments[j].name}) // inserer les string name commme ca get en O(1)

                    }
                }
            }
            for (let i = 0; i < this.attachments.length; i++) {
                let name = this.attachments[i].name
                console.log(name, uf.groupNumber(name), uf.numberOfMembre(name))
            }
            return uf
        },
        attachmentStyles(){ 
            let attachmentStyles = []
            for(let i = 0; i < this.emails.length; i++){
                let styles = []
                for (let j = 0; j < this.emails[i].attachments.length; j++) { // essayer de groupNumber et numberOfMembre directement avec le name
                let name = this.emails[i].attachments[j].name
                    if(this.clusterOfAttachments.numberOfMembre(name) > 1){
                        styles.push(colors[this.clusterOfAttachments.groupNumber(name) % colors.length])
                    } else {
                        styles.push(null)
                    }
                }
                attachmentStyles.push(styles)
            }
            return attachmentStyles
        }
    },

}
</script>

<style scoped>

form {
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
    /* add a border */
}
</style>