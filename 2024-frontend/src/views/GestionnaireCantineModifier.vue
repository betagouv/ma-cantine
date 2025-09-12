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
  if (form.hasSiret === "no-siret") delete form.siret
  canteenService
    .updateCanteen(form, canteenId)
    .then((response) => {
      if (response.id) goToCanteenPage(response)
      else store.notifyServerError()
    })
    .catch((e) => store.notifyServerError(e))
}

/* After canteen is saved */
const goToCanteenPage = (canteen) => {
  const canteenUrl = urlService.getCanteenUrl(canteen)
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: canteenUrl },
  })
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
      @cancel="(id) => goToCanteenPage(canteenId)"
    />
    <p v-else>
      Une erreur est survenue,
      <AppLinkRouter :to="{ name: 'DashboardManager' }" title="revenir à la page précédente" />
    </p>
  </section>
  <section class="fr-container fr-background-alt--red-marianne fr-p-3w fr-mt-2w fr-grid-row fr-grid-row--center">
    <div class="fr-col-12 fr-col-lg-7 fr-background-default--grey fr-p-2w fr-p-md-7w">
      <h2 class="fr-h5 fr-text-default--error">
        <span class="mdi mdi-delete"></span>
        Supprimer cet établissement
      </h2>
      <p class="fr-mb-0">
        Vous ne souhaitez plus faire apparaître cet établissement sur la plateforme ma-cantine, vous pouvez le supprimer
        <AppLinkRouter :to="{ name: 'CanteenDeletion' }" title="en cliquant ici" />
      </p>
    </div>
  </section>
</template>
