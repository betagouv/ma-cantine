<script setup>
import { useRoute } from "vue-router"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

const route = useRoute()
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <h1>{{ route.meta.title }}</h1>
  </section>
  <CanteenEstablishmentForm establishment-data="" />
</template>
