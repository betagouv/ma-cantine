<template>
  <div>
    <h1>Mon tableau de bord</h1>

    <CanteenDashboard :diagnostics="diagnostics" :showResources="true"/>

    <button class="save-data" v-if="jwt" @click="saveDiagnostics">Sauvegarder mes données</button>
    <router-link class="save-data" v-else :to="{ name: 'ConnectPage' }">Sauvegarder mes données</router-link>
  </div>
</template>

<script>
  import CanteenDashboard from '@/components/CanteenDashboard';
  import { getDiagnostics } from '@/data/KeyMeasures.js';

  export default {
    components: {
      CanteenDashboard
    },
    props: ['diagnostics'],
    data() {
      return {
        jwt: localStorage.getItem('jwt')
      };
    },
    methods: {
      // TODO: remove save functionality from here, already would be saved
      async saveDiagnostics() {
        const jwt = this.jwt;
        const localDiagnostics = (await getDiagnostics()).localFlatDiagnostics;
        const response = await fetch(`${this.$api_url}/save-diagnostics`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+jwt
          },
          body: JSON.stringify({
            diagnostics: localDiagnostics
          })
        });

        if (response.status === 201) {
          alert("Vos données ont été sauvgardées")
        } else {
          const error = await response.json();
          console.log(error);
          alert("Une erreur est survenue, vous pouvez nous contacter directement à contact@egalim.beta.gouv.fr")
        }
      },
    }
  };
</script>

<style scoped lang="scss">
  h1 {
    font-weight: bold;
    font-size: 48px;
    color: $green;
    margin: 1em 0em;
  }

  .save-data {
    font-size: 1.2em;
    margin: auto;
    margin-top: 2em;
    border: none;
    background: $orange;
    border-radius: 1em;
    padding: 0.5em;
    color: $white;
    font-weight: bold;
    cursor: pointer;
    text-decoration: none;
  }

  a.save-data {
    display: block;
    width: max-content;
  }
</style>
