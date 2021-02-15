<template>
  <div class="notification is-success is-light" v-show="login_notification">
    <button
      class="delete"
      @click="login_notification = !login_notification"
    ></button>
    <p>{{ notification_message }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      login_notification: true,
    };
  },
  props: ["notification_message"],

  mounted() {
    setTimeout(() => {
      this.login_notification = false;
    }, 2000);
  },
};
</script>

<style>
</style>