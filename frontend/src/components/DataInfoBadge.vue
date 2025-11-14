<template>
  <DsfrBadge v-if="badge" :mode="badge.mode" :show-icon="false">
    <p class="ma-0 pa-0 text-uppercase">{{ badge.body }}</p>
  </DsfrBadge>
  <span v-else></span>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"
import diagnosticService from "../../../2024-frontend/src/services/diagnostics"

export default {
  name: "DataInfoBadge",
  components: { DsfrBadge },
  props: {
    currentYear: {
      default: false,
      type: Boolean,
    },
    inTeledeclaration: {
      type: Boolean,
      default: false,
    },
    inCorrection: {
      type: Boolean,
      default: false,
    },
    canteenAction: {
      type: String,
      default: null,
    },
  },
  computed: {
    badge() {
      const campaignDates = {
        inCorrection: this.inCorrection,
        inTeledeclaration: this.inTeledeclaration,
      }
      const badgeFromAction = diagnosticService.getBadge(this.canteenAction, campaignDates)
      const mode = this.currentYear ? "INFO" : badgeFromAction.type
      const body = this.currentYear ? "Année en cours" : badgeFromAction.label
      return {
        mode: mode !== null ? mode.toUpperCase() : mode,
        body,
      }
    },
  },
}
</script>
