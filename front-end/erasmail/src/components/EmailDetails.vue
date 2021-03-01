<template>
    <div>
        <p>{{email.sender_name}} {{email.sender_email}}</p>
        <p>{{email.subject}}</p>
        <p>{{readableSize(email.size)}}</p>
        <p>{{readableDate(email.received_at)}}</p>
        <p>{{email.attachments}}</p>
        <p>{{email.uid}}</p>
    </div>
</template>

<script>
const byteSize = require('byte-size')
export default {
    props: ['email'],
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
    }
}
</script>

<style>

</style>