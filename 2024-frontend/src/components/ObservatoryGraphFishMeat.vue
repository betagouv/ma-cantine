<script setup>
import { reactive } from "vue"
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"

const props = defineProps(["meatPercent", "fishPercent"])
const title = "Viandes et volailles + produits d’aquacultures"

/* Graph properties */
const objectives = [
  { name: "60%", value: 60 },
  { name: "100% pour les restaurants d’état", value: 100 },
]
const stats = reactive([props.meatPercent + props.fishPercent])
</script>
<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[props.meatPercent, props.fishPercent]">
    <GraphGauge :objectives="objectives" :stats="stats" />
  </GraphBase>
</template>
