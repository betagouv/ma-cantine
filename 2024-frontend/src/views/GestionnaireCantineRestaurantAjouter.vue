<script setup>
import { ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens"
import urlService from "@/services/urls"
import AppRessources from "@/components/AppRessources.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenEstablishmentForm from "@/components/CanteenEstablishmentForm.vue"

/* Router and Store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()

/* Save canteen */
const forceRerender = ref(0)

const saveCanteen = (props) => {
  const { form, action } = props
  canteensService
    .createCanteen(form)
    .then((canteenCreated) => {
      const centralType = ["central", "central_serving"]
      const stayOnCreationPage = canteenCreated.id && action === "stay-on-creation-page"
      const redirect = canteenCreated.id && action === "go-to-canteen-page"
      const isCentral = centralType.includes(form.productionType)
      if (!canteenCreated.id) store.notifyServerError()
      if (stayOnCreationPage) resetForm(canteenCreated.name)
      if (redirect && !isCentral) goToNewCanteenPage(canteenCreated)
      if (redirect && isCentral) goToSatellitesPage(canteenCreated)
    })
    .catch((e) => {
      store.notifyServerError(e)
    })
}

/* After canteen is saved */
const goToNewCanteenPage = (canteen) => {
  const canteenUrl = urlService.getCanteenUrl(canteen)
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: canteenUrl },
  })
}

const goToSatellitesPage = (canteen) => {
  const canteenUrl = urlService.getCanteenUrl(canteen)
  router.replace({
    name: "GestionnaireCantineGroupeGerer",
    params: { canteenUrlComponent: canteenUrl },
  })
}

const resetForm = (name) => {
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
        En accord avec
        <a href="https://www.legifrance.gouv.fr/loda/id/JORFTEXT000046335035/" target="_blank">
          l’arrêté du 14 septembre 2022
        </a>
        , chaque restaurant collectif doit être inscrit sur
        <em>ma cantine</em>
        : étape préalable à la déclaration des informations nécessaires à la réalisation du bilan statistique national.
        Veuillez remplir ce formulaire pour l’ensemble des restaurants collectifs dont vous avez la charge.
      </p>
      <p class="fr-mb-0 fr-text--bold">
        Tout restaurant satellite doit être rattaché à la cuisine centrale qui livre les repas. Ainsi, la cuisine
        centrale doit être préalablement inscrite sur
        <em>ma cantine.</em>
      </p>
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
