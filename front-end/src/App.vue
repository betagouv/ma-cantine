<template>
  <TheNavbar/>

  <router-view/>

  <TheFooter/>
</template>

<script>
// @ is an alias to /src
import TheNavbar from '@/components/TheNavbar.vue'
import TheFooter from '@/components/TheFooter.vue'

export default {
  components: {
    TheNavbar,
    TheFooter,
  },
  watch: {
    '$route' (to) {
      const suffix = "ma-cantine.beta.gouv.fr";
      document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix;
    }
  },
}
</script>

<style>
@font-face {
  font-family: "Marianne";
  src: local("Marianne"),
    url('~@/assets/fonts/Marianne/Marianne-Regular.woff2') format("woff2"),
    url('~@/assets/fonts/Marianne/Marianne-Regular.woff') format("woff");
}

#app {
  font-family: Marianne, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

ul {
  list-style-type: none;
  padding: 0;
}
</style>
