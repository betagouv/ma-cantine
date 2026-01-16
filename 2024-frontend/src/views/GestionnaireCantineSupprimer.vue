<script setup>
import { useRoute } from "vue-router"
import urlService from "@/services/urls.js"

/* Router */
const route = useRoute()
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
console.log(canteenId, canteenName)
</script>
<template>
  <div class="fr-col-12 fr-col-md-8 fr-mb-3w">
    <h1>{{ route.meta.title }} « {{ canteenName }} »</h1>
  </div>
</template>
