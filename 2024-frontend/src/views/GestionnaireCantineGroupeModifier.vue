<script setup>
import { ref, useTemplateRef } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import canteenService from "@/services/canteens.js"
import urlService from "@/services/urls"
import AppRessources from "@/components/AppRessources.vue"
import AppLoader from "@/components/AppLoader.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import CanteenFormGroupe from "@/components/CanteenFormGroupe.vue"

/* Router and Store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()

/* Component */
const forceRerender = ref(0)
const formRef = useTemplateRef("form-ref")
const errors = ref([])

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

/* Save group */
const saveGroup = (props) => {
  const { form } = props
  canteenService
    .updateCanteen(form, canteenId)
    .then((canteen) => {
      if(canteen.id) goToCanteenPage(canteen)
      else displayErrors(canteen)
    })
    .catch((e) => { store.notifyServerError(e) })
}

const displayErrors = (canteen) => {
  errors.value = canteen.list
  formRef.value.scrollIntoView({ behavior: "smooth" })
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
  <div ref="form-ref">
    <AppLoader v-if="loading" />
    <CanteenFormGroupe
      v-else-if="!loading && canteenData.id"
      :key="forceRerender"
      :showCancelButton="true"
      :establishment-data="canteenData"
      :errors="errors"
      @sendForm="(payload) => saveGroup(payload)"
      @cancel="goToCanteenPage(canteenData)"
    />
    <p v-else>
      Une erreur est survenue,
      <AppLinkRouter :to="{ name: 'DashboardManager' }" title="revenir à la page précédente" />
    </p>
  </div>
</template>
