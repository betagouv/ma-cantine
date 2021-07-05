<template>
  <div>
    <DashboardPage v-if="diagnostics" :diagnostics="diagnostics" />
    <EmptyDiagnosticPage v-else />
    <BetaTesterForm class="mt-12" />
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
      let diagnostics = this.$store.getters.getLocalDiagnostics()
      return {
        previous:
          diagnostics.find((x) => x.year === 2019) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2019 }),
        latest:
          diagnostics.find((x) => x.year === 2020) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2020 }),
        provisionalYear1:
          diagnostics.find((x) => x.year === 2021) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2021 }),
        provisionalYear2:
          diagnostics.find((x) => x.year === 2022) || Object.assign({}, Constants.DefaultDiagnostics, { year: 2022 }),
      }
    },
    isAuthenticated() {
      return !!this.$store.state.loggedUser
    },
  },
}
</script>
