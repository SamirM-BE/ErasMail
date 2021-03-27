<template>

    <footer class="footer px-3">
        <div class="columns is-vcentered">
            <div class="column main">
                <strong class="title is-5 has-text-primary">ErasMail</strong>
                <p>The source code is licensed Apache 2.0</p>
            </div>
            <div class="column is-flex is-justify-content-space-evenly">
                <a>Features</a>
                <a>Help</a>
                <a>Privacy</a>
                <a>Terms</a>
                <a href="mailto:info.erasmail@gmail.com">Contact</a>
            </div>
            <div class="column social">

                <span class="icon is-large is-pulled-right">
                    <i class="fab fa-lg fa-github"></i>
                </span>
                <span class="icon is-large is-pulled-right">
                    <i class="fab fa-lg fa-twitter"></i>
                </span>
                <span class="icon is-large is-pulled-right">
                    <i class="fab fa-lg fa-linkedin-in"></i>
                </span>
            </div>
        </div>
    </footer>
</template>

<script>

export default {
	name: "Footer",
	computed: {
	}
}
</script>


<style scoped>
.footer {
    padding: 0em;
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%
}


.social span {
    margin-left: 3%;
}

</style>