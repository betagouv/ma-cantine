<script setup>
import { ref, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"
import urlService from "@/services/urls"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

/* Router */
const route = useRoute()
const router = useRouter()

/* Stores */
const store = useRootStore()

/* Component */
const forceRerender = ref(0)
const canteenName = computed(() => urlService.getCanteenName(route.params.canteenUrlComponent))
const canteenId = computed(() => urlService.getCanteenId(route.params.canteenUrlComponent))

/* API */
const saveSatellite = (props) => {
  const { form, action } = props
  canteensService
    .addSatellite(form, canteenId.value)
    .then((canteenCreated) => {
      if (canteenCreated.id && action === "stay-on-creation-page") resetForm(canteenCreated.name)
      else if (canteenCreated.id && action === "go-to-canteen-page") goToNewCanteenPage(canteenCreated.id)
      else store.notifyServerError()
    })
    .catch((e) => {
      store.notifyServerError(e)
    })
}

/* After canteen is saved */
const goToNewCanteenPage = (id) => {
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: id },
  })
}

const resetForm = (name) => {
  store.notify({ message: `Cantine ${name} créée avec succès.` })
  window.scrollTo(0, 0)
  forceRerender.value++
}
</script>

<template>
  <section>
    <h1 class="fr-col-12 fr-col-md-8">
      {{ route.meta.title }}
      <br />
      à la cantine centrale {{ canteenName }}
    </h1>
  </section>
  <CanteenEstablishmentForm
    :showCreateButton="true"
    :addSatellite="true"
    :key="forceRerender"
    @sendForm="(payload) => saveSatellite(payload)"
  />
</template>
