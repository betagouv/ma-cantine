<template>
  <div>
    <h1 class="text-h4 font-weight-black my-6">Où en sommes nous sur les mesures de la loi ?</h1>

    <CanteenDashboard
      :diagnostics="diagnostics"
      :showResources="true"
      :canteen="originalCanteen"
      :singleColumn="true"
    />
  </div>
</template>

<script>
import CanteenDashboard from "@/components/CanteenDashboard"

export default {
  components: {
    CanteenDashboard,
  },
  props: ["diagnostics", "originalCanteen"],
  created() {
    document.title = `Améliorer - ${this.originalCanteen.name} - ${this.$store.state.pageTitleSuffix}`
  },
}
</script>
