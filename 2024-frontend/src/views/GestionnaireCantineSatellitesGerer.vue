<script setup>
import { computedAsync } from "@vueuse/core"
import { useRoute } from "vue-router"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls.js"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteen = computedAsync(async () => await canteenService.fetchCanteen(canteenId), {})
</script>
<template>
  <section>
    <div class="fr-col-1é fr-col-8">
      <h1>{{ route.meta.title }}</h1>
      <p v-if="!canteen.isCentralCuisine">
        Votre établissement n'est pas une cuisine centrale, vous ne pouvez pas associer de cuisines satellites. Pour
        modifier votre type d'établissement
        <AppLinkRouter
          title="cliquez-ici"
          :to="{ name: 'GestionnaireCantineModifier', params: route.canteenUrlComponent }"
        />
      </p>
      <p v-else>
        Lors de la création de votre établissement vous avez indiqué livrer des repas à
        {{ canteen.satelliteCanteensCount }} {{ canteen.satelliteCanteensCount > 1 ? "cantines" : "cantine" }}
      </p>
    </div>
  </section>
</template>
