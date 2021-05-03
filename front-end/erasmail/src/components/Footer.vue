<template>
    <footer class="footer">
        <div class="columns is-vcentered">
            <div class="column main">
                <strong class="title is-5 has-text-grey-lighter">ErasMail</strong>
                <p class="has-text-grey-lighter">The source code is licensed Apache 2.0</p>
            </div>
            <div class="column is-flex is-justify-content-space-evenly">
                <a href="#features" class="has-text-grey-lighter">Features</a>
                <a href="#faq" class="has-text-grey-lighter">Help</a>
                <a class="has-text-grey-lighter">Privacy</a>
                <a class=" has-text-grey-lighter">Terms</a>
                <a href="mailto:info.erasmail@gmail.com" class="has-text-grey-lighter">Contact</a>
            </div>
            <div class="column social">
                <a class="icon is-large is-pulled-right has-text-grey-lighter" href="https://github.com/SamirM-BE/ErasMail"
                    target="_blank">
                    <i class="fab fa-lg fa-github"></i>
                </a>
                <a class="icon is-large is-pulled-right has-text-grey-lighter" href="https://twitter.com/eras_mail"
                    target="_blank">
                    <i class="fab fa-lg fa-twitter"></i>
                </a>
                <a class="icon is-large is-pulled-right has-text-grey-lighter"
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