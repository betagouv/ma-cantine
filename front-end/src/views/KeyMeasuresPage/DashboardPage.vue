<template>
  <CanteenDashboard :diagnostics="diagnostics"/>
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
