<template>
  <DsfrBadge v-if="body">
    <p class="ma-0 pa-0 text-uppercase">{{ body }}</p>
  </DsfrBadge>
  <span v-else></span>
</template>
<script>
import DsfrBadge from "@/components/DsfrBadge"
export default {
  name: "DataInfoBadge",
  components: { DsfrBadge },
  props: {
    currentYear: {
      default: false,
      type: Boolean,
    },
    missingData: {
      default: false,
      type: Boolean,
    },
    readyToTeledeclare: {
      default: false,
      type: Boolean,
    },
  },
  computed: {
    body() {
      if (this.currentYear) return "Année en cours"
      if (this.missingData) return "Données à compléter"
      if (this.readyToTeledeclare) return "Bilan à télédéclarer"
      return null
    },
  },
}
</script>
