<template>
  <TheNavbar/>

  <div id="router-view">
    <router-view/>
  </div>

  <TheNewsletter/>

  <TheFooter/>

  <GiveFeedbackLink id="feedback"/>
</template>

<script>
import TheNavbar from '@/components/TheNavbar';
import TheFooter from '@/components/TheFooter';
import TheNewsletter from '@/components/TheNewsletter';
import GiveFeedbackLink from '@/components/GiveFeedbackLink';

export default {
  components: {
    TheNavbar,
    TheFooter,
    TheNewsletter,
    GiveFeedbackLink
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
  }

  #router-view {
    margin-top: 100px;
  }

  h1 {
    font-size: 37px;
    font-weight: 700;
  }

  h2 {
    font-weight: 700;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  #feedback {
    position: fixed;
    right: 10px;
    bottom: 10px;
  }

  @media (max-width: 1450px) {
    #router-view {
      margin-top: 150px;
    }
  }

  @media (max-width: 750px) {
    #router-view {
      margin-top: 0;
    }

    #feedback {
      position: relative;
    }
  }
</style>
