<script setup>
import { reactive } from "vue"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatFrancePercent"])
const title = "Pourcentage des viandes origine France"
const stats = reactive([props.meatFrancePercent])
</script>
<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="stats">
    <GraphGauge :stats="stats" />
  </GraphBase>
</template>
