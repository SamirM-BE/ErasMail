<template>
    <div class="modal" :class="{ 'is-active': showModal }">
        <div class="modal-background" @click="$emit('hideModal')"></div>
        <div class="modal-content">
            <form class="form box" v-on:submit.prevent="login">
                <!---->
                <EmailCheckbox v-for="(email, index) in emails" :key="index" :email="email"> </EmailCheckbox>
                <!---->
                <div class="field is-grouped">
                    <div class="control">
                        <button class="button is-danger" @click="$emit('removeEmails', {'Inbox':[1,2,3]} )">Remove</button>
                    </div>
                    <div class="control">
                        <button class="button is-light is-light" @click="$emit('hideModal')">Cancel</button>
                    </div>
                </div>
            </form>
        </div>
        <button class="modal-close" aria-label="close" @click="$emit('hideModal')"></button>
    </div>
</template>

<script>
import EmailCheckbox from "../components/EmailCheckbox";

export default {
    props: ['showModal', 'emails'],
    emits: ['hideModal', 'removeEmails'],
    components: {
        EmailCheckbox,
    },
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



</style>