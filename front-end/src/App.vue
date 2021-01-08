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
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway&display=swap');

#app {
  font-family: Raleway, Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
