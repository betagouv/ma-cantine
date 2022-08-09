<template>
  <div>
    <!-- TODO: breadcrumbs to lead back to DiagnosticPage for !isAuthenticated users ? -->
    <DashboardPage v-if="diagnostics" :diagnostics="diagnostics" />
    <EmptyDiagnosticPage v-else />
  </div>
</template>

<script>
import EmptyDiagnosticPage from "@/views/KeyMeasuresPage/EmptyDiagnosticPage"
import DashboardPage from "@/views/KeyMeasuresPage/DashboardPage"
import { diagnosticsMap } from "@/utils"

export default {
  components: {
    EmptyDiagnosticPage,
    DashboardPage,
  },
  computed: {
    diagnostics() {
      const diagnostics = this.$store.getters.getLocalDiagnostics()
      return diagnosticsMap(diagnostics)
    },
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
  },
}
</script>
