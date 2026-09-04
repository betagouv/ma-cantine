<template>
  <div>
    <DashboardPage :diagnostics="diagnostics" />
  </div>
</template>

<script>
import DashboardPage from "@/views/KeyMeasuresPage/DashboardPage"
import { diagnosticsMap } from "@/utils"

export default {
  components: {
    DashboardPage,
  },
  computed: {
    diagnostics() {
      const diagnostics = this.$store.getters.getLocalDiagnostics()
      return diagnosticsMap(diagnostics)
    },
  },
}
</script>
