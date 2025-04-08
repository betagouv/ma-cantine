<template>
  <DsfrBadge v-if="badge" :mode="badge.mode">
    <p class="ma-0 pa-0 text-uppercase">{{ badge.body }}</p>
  </DsfrBadge>
  <span v-else></span>
</template>

<script>
import DsfrBadge from "@/components/DsfrBadge"

const BADGE_LIST = [
  {
    // currentYear
    body: "Année en cours",
    mode: "INFO",
    actions: [],
  },
  {
    // missingData
    body: "Données à compléter",
    mode: "ERROR",
    actions: [
      "10_add_satellites",
      "35_fill_canteen_data",
      "18_prefill_diagnostic",
      "20_create_diagnostic",
      "30_fill_diagnostic",
    ],
  },
  {
    body: "En attente de la télédéclaration de votre livreur",
    mode: "WARNING",
    actions: ["90_nothing_satellite"],
  },
  {
    body: "Bilan non télédéclaré",
    mode: "ERROR",
    actions: ["45_did_not_teledeclare"],
  },
  {
    // readyToTeledeclare
    body: "Bilan à télédéclarer",
    mode: "ERROR",
    actions: ["40_teledeclare"],
  },
  {
    // hasActiveTeledeclaration
    body: "Bilan télédéclaré",
    mode: "SUCCESS",
    actions: ["91_nothing_satellite_teledeclared", "95_nothing"],
  },
]

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
    hasActiveTeledeclaration: {
      default: false,
      type: Boolean,
    },
    canteenAction: {
      type: String,
      default: null,
    },
  },
  computed: {
    badge() {
      if (this.currentYear) return BADGE_LIST[0]
      if (this.canteenAction)
        return BADGE_LIST.find((badge) => badge.actions && badge.actions.includes(this.canteenAction))
      if (this.hasActiveTeledeclaration) return BADGE_LIST[3]
      if (this.missingData) return BADGE_LIST[1]
      if (this.readyToTeledeclare) return BADGE_LIST[2]
      return null
    },
  },
}
</script>
