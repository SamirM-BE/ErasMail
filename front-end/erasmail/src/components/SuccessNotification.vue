<template>
  <div class="notification is-success is-light py-3" :style="positionStyle" v-show="show">
    <p class="m-4">{{ notificationMessage }}</p>
    <button class="delete" @click="show = !show"/>
  </div>
</template>

<script>
export default {
  data() {
    return {
      show: false,
    };
  },
  props: {
    notificationMessage: {
      type: String,
      required: true,
    },
    trigger: {
      type: Boolean,
      default: false,
    },
    delay: {
      type: Number,
      default: 2000,
    },
    positionStyle: {
      type: Object,
      default: () => ({ top: '3.25rem'}),
    },
  },
  created() {
    if (!this.trigger) {
      this.showNotification()
    }
  },
  watch:{
    trigger() {
      this.showNotification()
    }
  },
  methods: {
    showNotification(){
      this.show = true
      setTimeout(
        () => {
          this.show = false
        },
        this.delay
      )
    }
  }
};
</script>

<style scoped>
.notification{
  position: fixed;
  width: 100%;
  z-index: 999;
}
</style>