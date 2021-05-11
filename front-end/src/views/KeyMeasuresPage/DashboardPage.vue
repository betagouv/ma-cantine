<template>
  <div>
    <h1>Mon tableau de bord</h1>

    <CanteenDashboard :key="forceUpdate" :diagnostics="diagnostics" :showResources="true"/>

    <button class="save-data" v-if="jwt" @click="saveDiagnostics">Sauvegarder mes données</button>
    <router-link class="save-data" v-else :to="{ name: 'ConnectPage' }">Sauvegarder mes données</router-link>
  </div>
</template>

<script>
  import { defaultFlatDiagnostics, getDiagnostics } from '@/data/KeyMeasures.js';
  import CanteenDashboard from '@/components/CanteenDashboard';

  export default {
    components: {
      CanteenDashboard
    },
    data() {
      return {
        forceUpdate: 0,
        diagnostics: defaultFlatDiagnostics,
        jwt: localStorage.getItem('jwt')
      };
    },
    async mounted() {
      const diags = await getDiagnostics();
      this.diagnostics = diags.flatDiagnostics;
      // force the dashboard to re render after diagnostics are fetched
      this.forceUpdate = 1;
    },
    methods: {
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
