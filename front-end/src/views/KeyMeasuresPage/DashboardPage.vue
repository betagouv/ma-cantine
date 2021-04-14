<template>
  <div>
    <h1>Mon tableau de bord</h1>

    <CanteenDashboard :diagnostics="diagnostics"/>
  </div>
</template>

<script>
  import { diagnostics } from '@/data/KeyMeasures.js';
  import CanteenDashboard from '@/components/CanteenDashboard';

  export default {
    components: {
      CanteenDashboard
    },
    data() {
      return {
        diagnostics,
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
</style>
