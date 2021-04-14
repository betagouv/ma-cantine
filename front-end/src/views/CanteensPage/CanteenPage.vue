<template>
  <div id="canteen-dashboard">
    <CanteenDashboard :diagnostics="diagnostics"/>
  </div>
</template>

<script>
  import { getCanteenById } from '@/data/Canteens.js';
  import CanteenDashboard from '@/components/CanteenDashboard';

  export default {
    components: {
      CanteenDashboard
    },
    props: {
      id: String,
    },
    data() {
      return {
        diagnostics: getCanteenById(this.id).diagnostics,
      };
    },
  }
</script>

<style>
  #canteen-dashboard {
    padding: 1em 0.5em;
    max-width: 1170px;
    margin: auto;
  }
</style>
