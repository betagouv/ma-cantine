<script setup>
import { useRoute } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen"

const route = useRoute()
const canteenStore = useStoreCanteen()
canteenStore.setUrlComponent(route.params.canteenUrlComponent)
</script>

<template>
  <section>
    <h1 class="fr-col-12 fr-col-md-8">
      {{ route.meta.title }}
      <br />
      à la cantine centrale {{ canteenStore.name }}
    </h1>
  </section>
</template>
