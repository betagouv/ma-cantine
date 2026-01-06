<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls"
import AppRessources from "@/components/AppRessources.vue"
import AppLoader from "@/components/AppLoader.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenGroupForm from "@/components/CanteenGroupForm.vue"

/* Router and Store */
const route = useRoute()
const store = useRootStore()

/* Component */
const forceRerender = ref(0)

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


/* API */
const saveGroup = (props) => {
  const { form, action } = props
  console.log(form)
  console.log(action)
}
</script>

<template>
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-6 fr-mb-4w fr-mb-md-0">
      <h1>{{ route.meta.title }}</h1>
      <p>
        Les groupes de restaurants satellites vous permettent de gérer plusieurs établissements ensemble. Vous disposez d’une vue consolidée et pouvez réaliser une déclaration unique. Le montant total des achats du groupe est ensuite réparti automatiquement entre chaque restaurant satellite, au prorata de son nombre de couverts annuels. Les restaurants satellites peuvent être ajoutés ou retirés librement du groupe.
      </p>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">
          Annuaire des entreprises pour trouver le SIREN
        </a>
      </li>
    </AppRessources>
  </section>
  <AppLoader v-if="loading" />
  <CanteenGroupForm
    v-else-if="!loading && canteenData.id"
    :key="forceRerender"
    :showCancelButton="true"
    :establishment-data="canteenData"
    @sendForm="(payload) => saveGroup(payload)"
    @cancel="goToCanteenPage(canteenData)"
  />
  <p v-else>
    Une erreur est survenue,
    <AppLinkRouter :to="{ name: 'DashboardManager' }" title="revenir à la page précédente" />
  </p>
</template>
