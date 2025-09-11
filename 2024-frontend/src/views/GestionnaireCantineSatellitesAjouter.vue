<script setup>
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen"
import canteensService from "@/services/canteens"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

/* Router */
const route = useRoute()

/* Stores */
const canteenStore = useStoreCanteen()
canteenStore.setUrlComponent(route.params.canteenUrlComponent)

/* API */
const saveSatellite = (props) => {
  const { form, action } = props
  canteensService
    .addSatellite(form, canteenStore.id)
    .then((canteenCreated) => {
      console.log("canteenCreated", canteenCreated)
      console.log("action", action)
    })
}
</script>

<template>
  <section>
    <h1 class="fr-col-12 fr-col-md-8">
      {{ route.meta.title }}
      <br />
      à la cantine centrale {{ canteenStore.name }}
    </h1>
  </section>
  <CanteenEstablishmentForm
    :showCreateButton="true"
    :addSatellite="true"
    :key="forceRerender"
    @sendForm="(payload) => saveSatellite(payload)"
  />
</template>
