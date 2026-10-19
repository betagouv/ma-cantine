<script setup>
import { computed } from "vue"
import stringsService from "@/services/strings"
import GraphEgalim from "@/components/GraphEgalim.vue"

const props = defineProps(['diagnosticRecap'])

const approStats = computed(() => props.diagnosticRecap?.canteenDiagnosticApproStats)
const objectives = computed(() => props.diagnosticRecap?.notes)
</script>
<template>
  <GraphEgalim
    :egalim-percent="approStats.pourcentageEgalim"
    :bio-percent="approStats.pourcentageBio"
    :viandes-poissons-egalim-percent="approStats.pourcentageViandesVolaillesProduitsDeLaMerEgalim"
    :egalim-objective="objectives.egalimPercentObjective"
    :bio-objective="objectives.bioPercentObjective"
    :mention="`sur ${stringsService.prettyPercent(100)} du Total de vos achats`"
    :year="diagnosticRecap.year"
    :description-custom="`Pour le bilan ${diagnosticRecap.year}`"
  />
</template>
