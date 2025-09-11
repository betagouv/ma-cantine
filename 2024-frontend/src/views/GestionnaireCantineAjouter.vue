<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"
import AppRessources from "@/components/AppRessources.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

/* Router and Store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()

/* Save canteen */
const isSaving = ref(false)
const forceRerender = ref(0)

const saveCanteen = (props) => {
  const { form, action } = props
  isSaving.value = true
  canteensService
    .createCanteen(form)
    .then((canteenCreated) => {
      isSaving.value = false
      const centralType = ["central", "central_serving"]
      const stayOnCreationPage = canteenCreated.id && action === "stay-on-creation-page"
      const redirect = canteenCreated.id && action === "go-to-canteen-page"
      const isCentral = centralType.includes(form.productionType)
      if (!canteenCreated.id) store.notifyServerError()
      if (stayOnCreationPage) addNewCanteen(canteenCreated.name)
      if (redirect && !isCentral) goToNewCanteenPage(canteenCreated.id)
      if (redirect && isCentral) goToSatellitesPage(canteenCreated.id)
    })
    .catch((e) => {
      store.notifyServerError(e)
      isSaving.value = false
    })
}

/* After canteen is saved */
const goToNewCanteenPage = (id) => {
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: id },
  })
}

const goToSatellitesPage = (id) => {
  router.replace({
    name: "SatelliteManagement",
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
  <section class="fr-grid-row fr-grid-row--bottom">
    <div class="fr-col-12 fr-col-md-6 fr-mb-4w fr-mb-md-0">
      <h1>{{ route.meta.title }}</h1>
      <p>
        La mission de la plateforme
        <em>ma cantine</em>
        est de référencer toutes les cantines de France afin d’aider le ministère de l’agriculture à déployer sa
        transition alimentaire.
      </p>
      <p class="fr-mb-0">Remplissez le formulaire ci-dessous pour créer votre établissement.</p>
    </div>
    <div class="fr-col-offset-md-1"></div>
    <AppRessources>
      <li>
        <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">
          Annuaire des entreprises pour trouver le SIRET
        </a>
      </li>
      <li>
        <a href="https://annuaire-education.fr/" target="_blank">
          Annuaire des cantines scolaires pour trouver le SIRET
        </a>
      </li>
      <li>
        <AppLinkRouter
          :to="{ name: 'GestionnaireImportCantines' }"
          title="Créer plusieurs établissements via un fichier d’import"
        />
      </li>
    </AppRessources>
  </section>
  <CanteenEstablishmentForm
    :showCreateButton="true"
    :key="forceRerender"
    @sendForm="(payload) => saveCanteen(payload)"
  />
</template>
