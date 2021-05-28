<template>
  <div id="app">
    <v-app>
      <Header />

      <v-main>
        <v-container fluid :fill-height="!initialDataLoaded">
          <v-progress-circular
            indeterminate
            style="position: absolute; left: 50%; top: 50%"
            v-if="!initialDataLoaded"
          ></v-progress-circular>
          <router-view v-else class="mx-auto constrained" />
        </v-container>
      </v-main>

      <Footer />
    </v-app>
  </div>
</template>

<script>
import Header from "@/components/Header"
import Footer from "@/components/Footer"

export default {
  components: {
    Header,
    Footer,
  },
  computed: {
    initialDataLoaded() {
      return this.$store.state.initialDataLoaded
    },
  },
  watch: {
    $route(to) {
      const suffix = "ma-cantine.beta.gouv.fr"
      document.title = to.meta.title ? to.meta.title + " - " + suffix : suffix
    },
  },
}
</script>

<style>
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

.constrained {
  max-width: 1024px !important;
}
</style>
