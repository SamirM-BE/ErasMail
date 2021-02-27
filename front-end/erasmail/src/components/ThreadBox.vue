<template>
    <div class="box m-1">
        <h1>{{ subject }}</h1>
        <h3>Size: {{ readable_size }}</h3>
    </div>
</template>

<script>
import {
    convert_size
} from "../utils";

export default {
    props: ["subject", "size"],
    computed: {
    readable_size() {
      return convert_size(this.size);
    },
  },
}
</script>

<style scoped>
.box {
    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}
.box:hover {
  background-color: rgb(247, 245, 245);
}
</style>