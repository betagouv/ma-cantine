<script setup>
import { useRoute } from "vue-router"
import { computedAsync } from "@vueuse/core"
import { computed } from "vue"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"

/* Route */
const route = useRoute()

/* Header */
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenInformation = computedAsync(async () => await canteenService.fetchCanteen(canteenId), false)
const canteenBadgeId = computed(() => canteenId ? `ID : ${canteenId}` : null)
const canteenBadgeSiret = computed(() => canteenInformation.value?.siret ? `SIRET : ${canteenInformation.value.siret}` : null)
const canteenBadgeSiren = computed(() => canteenInformation.value?.sirenUniteLegale ? `SIREN : ${canteenInformation.value.sirenUniteLegale}` : null)
</script>

<template>
  <div>
    <h1>{{ canteenName }}</h1>
    <div class="ma-cantine--flex-start ma-cantine--flex-gap-1">
      <DsfrBadge v-if="canteenBadgeId" type="neutral" :label="canteenBadgeId" />
      <DsfrBadge v-if="canteenBadgeSiret" type="neutral" :label="canteenBadgeSiret" />
      <DsfrBadge v-if="canteenBadgeSiren" type="neutral" :label="canteenBadgeSiren" />
    </div>
    <slot></slot>
  </div>
</template>
