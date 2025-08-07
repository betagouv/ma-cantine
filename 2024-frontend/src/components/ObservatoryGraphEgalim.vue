<script setup>
import GraphBase from "@/components/GraphBase.vue"
import GraphGauge from "@/components/GraphGauge.vue"
defineProps(["approPercent"])
const title = "Télédéclarations qui ont atteint l'objectif EGalim"
</script>

<template>
  <h3 class="fr-h6 fr-mb-2w">{{ title }}</h3>
  <GraphBase :valuesToVerify="[approPercent]">
    <GraphGauge :stats="[approPercent]" />
  </GraphBase>
</template>
