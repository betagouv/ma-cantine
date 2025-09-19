<script setup>
import { useRoute } from "vue-router"
const route = useRoute()
</script>

<template>
  <section class="fr-col-12 fr-col-md-8">
    <h1>{{ route.meta.title }}</h1>
    <p>Retrouver toutes les informations de votre établissement.</p>
  </section>
</template>
