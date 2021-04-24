<template>
    <p>hey !</p>
    <Footer></Footer>
</template>

<script>
import Footer from "../components/Footer";

export default {
    name: "LandingPage",
    components: {
        Footer,
    },
}
</script>

<style scoped>
Footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: hsl(142, 52%, 98%);
}
</style>