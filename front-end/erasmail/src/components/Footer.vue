<template>
    <footer class="footer">
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
                <a class="icon is-large is-pulled-right has-text-grey-dark" href="https://github.com/SamirM-BE/ErasMail"
                    target="_blank">
                    <i class="fab fa-lg fa-github"></i>
                </a>
                <a class="icon is-large is-pulled-right has-text-grey-dark" href="https://twitter.com/eras_mail"
                    target="_blank">
                    <i class="fab fa-lg fa-twitter"></i>
                </a>
                <a class="icon is-large is-pulled-right has-text-grey-dark"
                    href="https://www.linkedin.com/company/erasmail" target="_blank">
                    <i class="fab fa-lg fa-linkedin-in"></i>
                </a>
            </div>
        </div>
    </footer>
</template>

<script>

export default {
	name: "Footer",
}
</script>


<style scoped>
.social span {
    margin-left: 3%;
}
</style>