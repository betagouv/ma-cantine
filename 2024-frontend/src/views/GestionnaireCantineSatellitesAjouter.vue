<script setup>
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

const route = useRoute()
const canteenStore = useStoreCanteen()
canteenStore.setUrlComponent(route.params.canteenUrlComponent)

const saveCanteen = (payload) => {
  console.log("payload", payload)
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
    :key="forceRerender"
    @sendForm="(payload) => saveCanteen(payload)"
  />
</template>
