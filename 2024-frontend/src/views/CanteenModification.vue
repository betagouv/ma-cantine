<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

/* Router and Store */
const route = useRoute()

/* Get establishemnt infos */
const canteenId = computed(() => route.params.canteenUrlComponent.split("--")[0])
console.log("canteenId", canteenId)
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <h1>{{ route.meta.title }}</h1>
  </section>
  <CanteenEstablishmentForm establishment-data="" />
</template>
