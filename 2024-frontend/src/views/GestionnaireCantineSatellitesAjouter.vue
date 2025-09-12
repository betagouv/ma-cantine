<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useStoreCanteen } from "@/stores/canteen"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

/* Router */
const route = useRoute()
const router = useRouter()

/* Stores */
const canteenStore = useStoreCanteen()
canteenStore.setUrlComponent(route.params.canteenUrlComponent)
const store = useRootStore()

/* Render */
const forceRerender = ref(0)

/* API */
const saveSatellite = (props) => {
  const { form, action } = props
  canteensService
    .addSatellite(form, canteenStore.id)
    .then((canteenCreated) => {
      if (canteenCreated.id && action === "stay-on-creation-page") addNewCanteen(canteenCreated.name)
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

const addNewCanteen = (name) => {
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
      à la cantine centrale {{ canteenStore.name }}
    </h1>
  </section>
  <CanteenEstablishmentForm
    :showCreateButton="true"
    :addSatellite="true"
    :key="forceRerender"
    @sendForm="(payload) => saveSatellite(payload)"
  />
</template>
