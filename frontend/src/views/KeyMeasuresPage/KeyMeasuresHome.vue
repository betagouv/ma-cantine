<template>
  <div>
    <DashboardPage v-if="diagnostics" :diagnostics="diagnostics" />
    <EmptyDiagnosticPage v-else />
    <BetaTesterForm />
  </div>
</template>

<script>
import Constants from "@/constants"
import EmptyDiagnosticPage from "@/views/KeyMeasuresPage/EmptyDiagnosticPage"
import DashboardPage from "@/views/KeyMeasuresPage/DashboardPage"
import BetaTesterForm from "@/components/BetaTesterForm"

export default {
  components: {
    EmptyDiagnosticPage,
    DashboardPage,
    BetaTesterForm,
  },
  computed: {
    diagnostics() {
      let diagnosis = this.isAuthenticated ? this.serverDiagnostics : this.localDiagnostics
      return {
        previous:
          diagnosis.find((x) => x.year === 2019) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
        latest:
          diagnosis.find((x) => x.year === 2020) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
      }
    },
    serverDiagnostics() {
      return this.$store.state.userCanteens[0].diagnosis
    },
    localDiagnostics() {
      return this.$store.getters.getLocalDiagnosis()
    },
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
  },
}
</script>
