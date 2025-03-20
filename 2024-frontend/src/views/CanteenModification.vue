<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"
import AppLoader from "@/components/AppLoader.vue"

/* Router and Store */
const route = useRoute()
const store = useRootStore()

/* Get establishemnt infos */
const canteenData = ref({})
const loading = ref(true)
const canteenId = route.params.canteenUrlComponent.split("--")[0]
canteenService
  .fetchCanteen(canteenId)
  .then((response) => {
    loading.value = false
    if (response.id) canteenData.value = response
    else store.notifyServerError()
  })
  .catch((e) => store.notifyServerError(e))
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <h1>{{ route.meta.title }}</h1>
  </section>
  <AppLoader v-if="loading" />
  <p v-else-if="!loading && !canteenData.id">Erreur retourne à la page précédente ?</p>
  <CanteenEstablishmentForm v-else-if="!loading && canteenData.id" :establishment-data="canteenData" />
</template>
