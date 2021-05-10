<template>
  <div>
    <DashboardPage v-if="haveDiagnosticResults"/>
    <EmptyDiagnosticPage v-else/>
    <BetaTesterForm />
  </div>
</template>

<script>
  import { haveDiagnosticResults } from '@/data/KeyMeasures.js';
  import EmptyDiagnosticPage from '@/views/KeyMeasuresPage/EmptyDiagnosticPage';
  import DashboardPage from '@/views/KeyMeasuresPage/DashboardPage';
  import BetaTesterForm from '@/components/BetaTesterForm';

  export default {
    components: {
      EmptyDiagnosticPage,
      DashboardPage,
      BetaTesterForm
    },
    data() {
      return {
        haveDiagnosticResults: null
      };
    },
    async mounted() {
      this.haveDiagnosticResults = await haveDiagnosticResults();
    }
  }
</script>
