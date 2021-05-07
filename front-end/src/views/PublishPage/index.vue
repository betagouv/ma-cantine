<template>
  <div>
    <nav id="steps-nav">
      <router-link :to="{ name: 'CanteenInfo' }" class="nav-item">Cantine informations</router-link>
      <template v-for="measure in keyMeasures" :key="measure.id">
        <router-link :to="{ name: 'PublishMeasurePage', params: { id: measure.id } }" class="nav-item">
          {{ measure.shortTitle }}
        </router-link>
      </template>
      <router-link :to="{ name: 'SubmitPublicationPage' }" class="nav-item">Publication des données</router-link>
    </nav>

    <div id="router-view">
      <router-view :key="$route.fullPath" :routeProps="routeProps"/>
    </div>
  </div>
</template>

<script>
  import keyMeasures from '@/data/key-measures.json'

  export default {
    created() {
      if (this.jwt) {
        return this.fetchPrefilledPublication();
      }
      this.$router.replace({ name: 'LandingPage' });
    },
    data() {
      return {
        keyMeasures,
        prefilledPublication: {},
        jwt: localStorage.getItem('jwt')
      };
    },
    methods: {
      async fetchPrefilledPublication() {
        const prefilledPublication = await fetch(`${this.$api_url}/get-prefilled-publication`, {
          method: "GET",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + this.jwt
          },
        });

        return this.prefilledPublication = await prefilledPublication.json();
      }
    },
    computed: {
      routeProps() {
        return this.$route.name === "PublishMeasurePage" ? this.prefilledPublication.diagnostics : this.prefilledPublication.canteen;
      }
    }
  }
</script>

<style scoped lang="scss">
  #router-view {
    max-width: 850px;
    margin: 30px auto;
    padding: 50px;
    border-radius: 2em;
    background-color: $dark-white;
  }

  #steps-nav {
    display: flex;
    justify-content: space-around;
    max-width: 1170px;
    margin: 8em auto 0 auto;
  }

  a {
    text-decoration: none;
  }

  .nav-item {
    color: $grey;
    padding: 10px;
    border-radius: 20px;
    margin: 0 3px;
  }

  .nav-item:hover, .router-link-exact-active {
    background-color: $light-orange;
  }

  @media (max-width: 750px) {
    #steps-nav {
      flex-direction: column;
      margin-top: 2em;
    }

    .nav-item {
      margin: 3px 0;
    }
  }
</style>
