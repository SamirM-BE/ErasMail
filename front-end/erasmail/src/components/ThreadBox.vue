<template>
    <div class="box m-1 py-1 px-3">
        <strong>{{ subject }}</strong>
        <h3>Size: {{ readable_size }}</h3>
    </div>
</template>

<script>
const byteSize = require('byte-size')

export default {
    props: ["subject", "size"],
    computed: {
    readable_size() {
      let size_unit = byteSize(this.size)
      return `${size_unit.value} ${size_unit.unit}`;
    },
  },
}
</script>

<style scoped>
.box {
    /* border-radius: 15px; */
    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}
.box:hover {
  background-color: rgb(247, 245, 245);
}
</style>