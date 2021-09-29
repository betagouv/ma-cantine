<template>
  <div>
    <DashboardPage v-if="diagnostics" :diagnostics="diagnostics" />
    <EmptyDiagnosticPage v-else />
    <BetaTesterForm class="mt-12" />
  </div>
</template>

<script>
import EmptyDiagnosticPage from "@/views/KeyMeasuresPage/EmptyDiagnosticPage"
import DashboardPage from "@/views/KeyMeasuresPage/DashboardPage"
import BetaTesterForm from "@/components/BetaTesterForm"
import { diagnosticsMap } from "@/utils"

export default {
  components: {
    EmptyDiagnosticPage,
    DashboardPage,
    BetaTesterForm,
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
