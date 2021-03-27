<template>
  <div class="modal" :class="{ 'is-active': showModal }">
    <div class="modal-background" @click="hideModal()"></div>
    <div class="modal-card">
      <header class="modal-card-head has-background-primary-dark">
        <h1 class="modal-card-title"><strong class="has-text-white">{{ threadSubject }}</strong></h1>

        <button class="delete" aria-label="close" @click="hideModal()"></button>
      </header>
      <section class="modal-card-body pt-0 has-background-primary-light">
        <div class="duplicate-message has-background-danger-light has-text-danger-dark has-text-centered"
             v-if="numberOfDuplicate != 0">
          <p v-if="numberOfDuplicate==1"> There is {{ numberOfDuplicate }} potential duplicate attachment</p>
          <p v-else> There are {{ numberOfDuplicate }} potential duplicate attachments</p>
        </div>
        <EmailForm :class="{'mt-4': numberOfDuplicate == 0, 'mt-5-2': numberOfDuplicate !== 0}" :emails="emails"
                   :attachmentStylesList="attachmentStyles" :reset="!showModal" @checked-emails="updateCheckedEmails">
        </EmailForm>
      </section>
      <footer class="modal-card-foot has-background-primary-dark">
        <div class="dropdown is-up" :class="{'is-active': showDropdown}">
          <div class="dropdown-trigger" @click="showDropdown = !showDropdown">
            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu">
              <span>{{ selectedAction }}</span>
              <span class="icon is-small">
                                <i class="fas fa-angle-down" aria-hidden="true"></i>
                            </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <a class="dropdown-item" :class="{'is-active': selectedAction === removeEmail}"
                 @click="selectAction(removeEmail)">
                <p>{{ removeEmail }}</p>
              </a>
              <!-- <hr class="dropdown-divider"> -->
              <a class="dropdown-item" :class="{'is-active': selectedAction === removeAttachment}"
                 v-if="selectedEmailsHasAttachment != false" @click="selectAction(removeAttachment)">
                <p>{{ removeAttachment }}</p>
              </a>
            </div>
          </div>
        </div>
        <button class="button is-danger ml-1" :disabled="selectedAction === 'Select an action'"
                @click="executeAction()">Execute
        </button>
        <div>
          <p class="has-text-white"> Selected size : {{ readableSize(selectedSize) }} / {{ readableSize(maxSize) }}</p>
          <!-- / ==> out of -->
          <progress class="progress is-small is-primary" :value="selectedSize" :max="maxSize"></progress>
        </div>

      </footer>
    </div>
  </div>
</template>

<script>
import EmailForm from "./EmailForm";
import {UnionFind} from "../utils/UnionFind";

const byteSize = require('byte-size')
const stringSimilarity = require("string-similarity")
const randomColor = require('random-color')

const excludeType = ['mp3', 'wma', 'm4a', 'png', 'jpeg', 'jpg'] // audio and images files never considered as duplicate

function isDuplicate(attachmentName1, attachmentName2) {
  attachmentName1 = attachmentName1.split('.')
  attachmentName2 = attachmentName2.split('.')

  let fileType1 = attachmentName1.pop().toLowerCase()
  let fileType2 = attachmentName2.pop().toLowerCase()

  if (fileType1 !== fileType2 || excludeType.includes(fileType1)) {
    return false
  }

  // this regex is used to remove all characters useless at the end of the filename
  // like _V-1, v_1, 3, ...
  // it done in order to maximizer the similarity because `report v_1` and `report v_2` may be duplicate
  const regex_delete = /( |-|_)v(|-|_)[0-9^)]+|( |-|_)\([0-9^)]+\)/ig
  // this regex is used to replace all _ or - by a space
  // it done in order to maximizer the similarity because `internship report` and `internship_report` may be duplicate
  const regex_space = /-|_/ig

  let fileName1 = attachmentName1.join('.').replace(regex_delete, '').replace(regex_space, ' ').trim()
  let fileName2 = attachmentName2.join('.').replace(regex_delete, '').replace(regex_space, ' ').trim()

  return fileName1.includes(fileName2) ||
      fileName2.includes(fileName1) ||
      stringSimilarity.compareTwoStrings(fileName1, fileName2) >= 0.8
}

export default {
  data() {
    return {
      checkedEmails: [],
      showDropdown: false,
      selectedAction: 'Select an action',
      removeEmail: 'Delete emails',
      removeAttachment: 'Delete attachments'
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
  emits: ['hide-modal', 'delete'],
  watch: {
    selectedEmailsHasAttachment(newValue) {
      if (newValue) {
        this.selectedAction = 'Select an action'
      } else {
        this.selectedAction = this.removeEmail
      }
    },
    attachments(newValue) {
      if (!newValue.length) {
        this.selectedAction = this.removeEmail
      }
    }
  },
  computed: {
    selectedSize() {
      let size = 0
      this.checkedEmails.forEach((emailIdx) => size += this.emails[emailIdx].size)
      return size;
    },
    maxSize() {
      let size = 0
      for (let i = 0; i < this.emails.length; i++) {
        size += this.emails[i].size
      }
      return size;
    },
    selectedEmailsHasAttachment() {
      if (!this.checkedEmails.length) {
        return undefined
      }
      for (let i = 0; i < this.checkedEmails.length; i++) {
        let index = this.checkedEmails[i]
        let email = this.emails[index]
        if (email.attachments.length) {
          return true
        }
      }
      return false
    },
    attachments() {
      let attachments = []
      for (let i = 0; i < this.emails.length; i++) {
        let attach = this.emails[i].attachments
        attach.forEach((item) => item.id = i)
        attachments.push(...attach)
      }
      return attachments
    },
    clusterOfAttachments() {
      let uf = new UnionFind(this.attachments.length)
      for (let i = 0; i < this.attachments.length; i++) {
        for (let j = i + 1; j < this.attachments.length; j++) {
          if (this.attachments[i].id !== this.attachments[j].id && isDuplicate(this.attachments[i].name, this.attachments[j].name)) {
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
      for (let i = 0; i < this.attachments.length; i++) {
        colors.push(randomColor().hexString())
      }
      return colors
    },
  },
  components: {
    EmailForm,
  },
  methods: {
    updateCheckedEmails(newCheckedEmails) {
      this.checkedEmails = newCheckedEmails
    },
    readableSize(size) {
      size = byteSize(size)
      return `${size.value} ${size.unit}`;
    },
    hideModal() {
      this.checkedEmails = []
      this.showDropdown = false,
          this.selectedAction = 'Select an action',
          this.$emit('hide-modal')
    },
    selectAction(action) {
      this.showDropdown = false
      this.selectedAction = action
    },
    executeAction() {
      if (this.selectedAction == this.removeEmail || this.selectedAction == this.removeAttachment) {
        this.remove()
      } else {
        console.log('other actions coming soon')
      }
    },

    remove() {
      let toRemove = {
        count: 0,
        uids: {},
        onlyAttachments: false,
      }
      toRemove.count = this.checkedEmails.length
      for (let i = 0; i < this.checkedEmails.length; i++) {
        let index = this.checkedEmails[i]

        let email = this.emails[index]

        let uids = toRemove.uids[email.folder] || []
        uids.push(email.uid)
        toRemove.uids[email.folder] = uids
      }
      if (this.selectedAction == this.removeEmail) {
        this.$emit('delete', toRemove)
      } else { // this.selectedAction == this.removeAttachment
        toRemove.onlyAttachments = true
        this.$emit('delete', toRemove)
      }
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
  left: 0;
  width: 100%;
  z-index: 1;
}

.mt-5-2 {
  margin-top: 2.5rem;
}

</style>