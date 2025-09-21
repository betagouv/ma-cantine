<script setup>
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteen = computedAsync(async () => await canteenService.fetchCanteen(canteenId), {})
const satellites = computedAsync(async () => await canteenService.fetchSatellites(canteenId), {})
</script>
<template>
  <section>
    <pre>{{ satellites }}</pre>
    <div class="fr-col-12 fr-col-md-8">
      <h1>{{ route.meta.title }}</h1>
      <p v-if="!canteen.isCentralCuisine">
        Votre établissement n'est pas une cuisine centrale, vous ne pouvez pas associer de cuisines satellites. Pour
        modifier votre type d'établissement
        <AppLinkRouter
          title="cliquez-ici"
          :to="{ name: 'GestionnaireCantineModifier', params: route.canteenUrlComponent }"
        />
      </p>
    </div>
    <div class="fr-grid-row fr-grid-row--middle" v-if="canteen.isCentralCuisine">
      <p class="fr-col-12 fr-col-md-6 fr-mb-0">
        {{ satellites.count }} / {{ canteen.satelliteCanteensCount }}
        {{ satellites.count > 1 ? "cantines satellites renseignées" : "cantine satellite renseignée" }}
      </p>
      <div class="fr-col-12 fr-col-md-6 fr-grid-row fr-grid-row--right">
        <router-link :to="{ name: 'GestionnaireCantineSatellitesAjouter', params: route.canteenUrlComponent }">
          <DsfrButton label="Ajouter une cantine satellite" />
        </router-link>
      </div>
    </div>
  </section>
</template>
