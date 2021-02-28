<template>
    <div class="box field">
        <div class="control">
            <label class="checkbox">
                <input type="checkbox">
                 <p> {{email.subject}} {{email.sender_email}} </p>
                 <p> {{email.attachments}} </p> 
            </label>
        </div>
    </div>
</template>

<script>
export default {
    props: ['email'],
}
</script>

<style scoped>
.box {
    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}
</style>