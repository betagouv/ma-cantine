<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls"
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
const canteenId = urlService.getCanteenId(route.params.canteenUrlComponent)

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
  if (form.hasSiret === "no-siret") delete form.siret
  canteenService
    .updateCanteen(form, canteenId)
    .then((canteen) => {
      if(canteen.id) goToCanteenPage(canteen)
      else store.notifyServerError()
  })
    .catch((e) => store.notifyServerError(e))
}

/* Page redirection */
const goToCanteenPage = (canteen) => {
  const canteenPage = {
    name: "GestionnaireCantineGerer",
    params: { canteenUrlComponent: urlService.getCanteenUrl(canteen) },
  }
  const redirectPage = route.query['redirection']
  router.replace(redirectPage || canteenPage)
}

</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <h1>{{ route.meta.title }}</h1>
    <AppLoader v-if="loading" />
    <CanteenEstablishmentForm
      v-else-if="!loading && canteenData.id"
      :establishment-data="canteenData"
      :showCancelButton="true"
      @sendForm="(payload) => saveCanteen(payload)"
      @cancel="goToCanteenPage(canteenData)"
    />
    <p v-else>
      Une erreur est survenue,
      <AppLinkRouter :to="{ name: 'DashboardManager' }" title="revenir à la page précédente" />
    </p>
  </section>
</template>
