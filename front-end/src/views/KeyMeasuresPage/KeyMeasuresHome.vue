<template>
  <div>
    <DashboardPage v-if="haveDiagnosticResults" :diagnostics="diagnostics"/>
    <EmptyDiagnosticPage v-else/>
    <BetaTesterForm />
  </div>
</template>

<script>
  import { getDiagnostics } from '@/data/KeyMeasures.js';
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
        diagnostics: null,
        haveDiagnosticResults: null
      };
    },
    async mounted() {
      const diags = await getDiagnostics();
      this.diagnostics = diags.flatDiagnostics;
      this.haveDiagnosticResults = (await getDiagnostics()).hasResults;
    },
  }
</script>
