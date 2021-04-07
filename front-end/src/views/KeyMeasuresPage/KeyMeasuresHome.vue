<template>
  <DashboardPage v-if="haveDiagnosticResults"/>
  <EmptyDiagnosticPage v-else/>
  <BetaTesterForm />
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
        haveDiagnosticResults: haveDiagnosticResults()
      };
    },
  }
</script>
