<script setup>
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen"
import canteensService from "@/services/canteens"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

const route = useRoute()
const canteenStore = useStoreCanteen()
canteenStore.setUrlComponent(route.params.canteenUrlComponent)

const saveCanteen = (payload) => {
  canteensService.addSatellite(payload.form, canteenStore.id).then((response) => {
    console.log("response", response)
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
    @sendForm="(payload) => saveCanteen(payload)"
  />
</template>
