<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"
import AppLoader from "@/components/AppLoader.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"

/* Router and Store */
const route = useRoute()
const router = useRouter()
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

/* Save canteen */
const saveCanteen = (props) => {
  const { form } = props
  canteenService
    .updateCanteen(form, canteenId)
    .then((response) => {
      if (response.id) goToCanteenPage(response.id)
      else store.notifyServerError()
    })
    .catch((e) => store.notifyServerError(e))
}

const goToCanteenPage = (id) => {
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: id },
  })
}
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <h1>{{ route.meta.title }}</h1>
  </section>
  <AppLoader v-if="loading" />
  <CanteenEstablishmentForm
    v-else-if="!loading && canteenData.id"
    :establishment-data="canteenData"
    @sendForm="(payload) => saveCanteen(payload)"
  />
  <p v-else>
    Une erreur est survenue,
    <AppLinkRouter :to="{ name: 'DashboardManager' }" title="revenir à la page précédente" />
  </p>
</template>
