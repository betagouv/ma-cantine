<template>
  <div>
    <h1>Mon tableau de bord</h1>

    <CanteenDashboard :diagnostics="diagnostics" :showResources="true"/>

    <p v-if="jwt"><i class="fas fa-check-square"></i> Vos données ont été sauvegardées</p>
    <router-link class="save-data" v-else :to="{ name: 'ConnectPage' }">Sauvegarder mes données</router-link>
  </div>
</template>

<script>
  import CanteenDashboard from '@/components/CanteenDashboard';

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
    display: block;
    width: max-content;
  }

  .fa-check-square {
    color: $green;
  }
</style>
