<template>
    <div class="email-detail px-2" @mouseover="hover = true" @mouseleave="hover = false">
        <strong>{{email.subject}}</strong>
        <p class="is-pulled-right">{{readableDate}}</p>

        <div class="icon-text">
            <span class="icon">
                <i class="far fa-address-card fa-sm"></i>
            </span>
            <span class="is-size-6" >{{email.sender_name}}<span v-if="email.sender_name">,</span> {{email.sender_email}}</span>
        </div>

        <ul class="ml-5">
            <li v-for="(attachment, index) in attachmentsSorted" :key="index">
                <div v-if="index < 2 || hover" class="is-flex is-justify-content-space-between my-1">
                    <span class="icon-text">
                        <span class="icon" :style="{ color: attachmentIconColor(attachment.name)}">
                            <i :class="[attachmentIcon(attachment.name)]"></i>
                        </span>
                        <span>{{attachment.name}} ({{readableSize(attachment.size)}} {{attachment.size}}) </span>
                    </span>
                    <span class="tag is-rounded has-text-black" v-if="attachmentStyle(index)"
                        :style="{'background-color': attachmentStyle(index)}"> Potential duplicate </span>
                </div>
            </li>
        </ul>

        <div class="icon-text">
            <span class="icon">
                <i class="fas fa-weight-hanging fa-xs"></i>
            </span>
            <span class="is-size-7">{{readableSize(email.size)}} {{email.size}}</span>
        </div>
    </div>
</template>

<script>
const byteSize = require('byte-size')

const fileType = {
    // archive
    tar: 'archive',
    zip: 'archive',
    // audio
    mp3: 'audio',
    wma: 'audio',
    m4a: 'audio',
    // excel
    xls: 'excel',
    xlsx: 'excel',
    // image
    png: 'image',
    jpeg: 'image',
    jpg: 'image',
    // pdf
    pdf: 'pdf',
    // powerpoint
    ppt: 'powerpoint',
    pptx: 'powerpoint',
    // video
    mp4: 'video',
    avi: 'video',
    mov: 'video',
    // word
    doc: 'word',
    docx: 'word',
}
const icons = {
    archive: "far fa-file-archive",
    audio: "far fa-file-audio",
    excel: "far fa-file-excel",
    image: "far fa-file-image",
    pdf: "far fa-file-pdf",
    powerpoint: "far fa-file-powerpoint",
    video: "far fa-file-video",
    word: "far fa-file-word",
    other: "far fa-file-alt",
}

const iconColors = {
    excel: "green",
    image: "darkgray",
    pdf: "red",
    powerpoint: 'rgb(208, 68, 35)',
    video: "orange",
    word: "blue",
    other: "black",
}

export default {
    data() {
        return {
            hover: false,
        }
    },
    props: {
        email: {
            type: Object,
            required: true
        },
        attachmentStyles: Array,
    },
    computed:{
        attachmentsSorted() {
            var attachmentsList = this.email.attachments
            attachmentsList.sort((a, b) => b.size - a.size)
            return attachmentsList
        },
        readableDate() {
            let date = new Date(this.email.received_at)
            return `${(date.getMonth()+1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}/${date.getFullYear().toString().substr(-2)}`
        },
    },
    methods: {
        readableSize(size) {
            size = byteSize(size)
            return `${size.value} ${size.unit}`;
        },
        attachmentStyle(index) {
            if (this.attachmentStyles) {
                return this.attachmentStyles[index]
            }
            return null
        },
        attachmentIcon(attachmentName){
            let type = fileType[attachmentName.split('.').pop()]
            if (type){
                return icons[type]
            }
            return icons.other
        },
        attachmentIconColor(attachmentName){
            let type = fileType[attachmentName.split('.').pop()]
            if (type){
                return iconColors[type]
            }
            return iconColors.other
        }
    }
}
</script>

<style>
.tag{
    float: right;
}

.test{
    color: lightgreen;
}

</style>