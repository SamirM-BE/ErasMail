<template>
  <div class="notification is-success is-light" v-show="notification_show">
    <button
      class="delete"
      @click="notification_show = !notification_show"
    ></button>
    <p>{{ notification_message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      notification_show: true,
    };
  },
  props: ["notification_message"],

  mounted() {
    setTimeout(() => {
      this.notification_show = false;
    }, 2000);
  },
};
</script>

<style scoped>
.notification{
  position: absolute;
  top: 0;
  width: 100%;
}
</style>