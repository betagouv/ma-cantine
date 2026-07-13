<script setup>
import { useRoute } from "vue-router"
import { computedAsync } from "@vueuse/core"
import urlService from "@/services/urls.js"
import canteenService from "@/services/canteens.js"

const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenInformation = computedAsync(async () => {
  return await canteenService.fetchCanteen(canteenId)
}, false)
</script>

<template>
  <div>
    <h1>{{ canteenName }}</h1>
    <div class="ma-cantine--flex-start ma-cantine--flex-gap-1">
      <DsfrBadge v-if="canteenInformation.id" type="neutral" :label="`ID : ${canteenInformation.id}`" />
      <DsfrBadge v-if="canteenInformation.siret" type="neutral" :label="`SIRET : ${canteenInformation.siret}`" />
      <DsfrBadge v-if="canteenInformation.sirenUniteLegale" type="neutral" :label="`SIREN : ${canteenInformation.sirenUniteLegale}`" />
    </div>
    <slot></slot>
  </div>
</template>
