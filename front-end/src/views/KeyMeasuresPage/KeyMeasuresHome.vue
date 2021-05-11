<template>
  <div>
    <DashboardPage v-if="diagnostics" :diagnostics="diagnostics"/>
    <EmptyDiagnosticPage v-else/>
    <BetaTesterForm />
  </div>
</template>

<script>
  import { getDiagnosticsForDashboard } from '@/data/KeyMeasures.js';
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
        diagnostics: null
      };
    },
    async mounted() {
      this.diagnostics = await getDiagnosticsForDashboard();
    },
  }
</script>
