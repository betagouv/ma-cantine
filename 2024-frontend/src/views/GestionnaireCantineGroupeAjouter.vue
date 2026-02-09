<script setup>
import { ref, useTemplateRef } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import documentation from "@/data/documentation.json"
import canteensService from "@/services/canteens"
import urlService from "@/services/urls"
import AppRessources from "@/components/AppRessources.vue"
import CanteenFormGroupe from "@/components/CanteenFormGroupe.vue"

/* Router and Store */
const route = useRoute()
const router = useRouter()
const store = useRootStore()

/* Component */
const forceRerender = ref(0)
const errors = ref([])
const formRef = useTemplateRef("form-ref")

/* Save group */
const saveGroup = (props) => {
  const { form, action } = props
  form.siret = null // SIRET is required to create a canteen
  canteensService
    .createCanteen(form)
    .then((canteenCreated) => {
      if (!canteenCreated.id) errorCreateCanteen(canteenCreated)
      else successCreateCanteen(canteenCreated, action)
    })
    .catch((e) => { store.notifyServerError(e) })
}

const successCreateCanteen = (canteenCreated, action) => {
  const stayOnCreationPage = canteenCreated.id && action === "stay-on-creation-page"
  const redirect = canteenCreated.id && action === "go-to-canteen-page"
  if (stayOnCreationPage) resetForm(canteenCreated.name)
  if (redirect) goToNewCanteenPage(canteenCreated)
}

const errorCreateCanteen = (canteenCreated) => {
  errors.value = canteenCreated.list
  formRef.value.scrollIntoView({ behavior: "smooth" })
}

/* After canteen is saved */
const goToNewCanteenPage = (canteen) => {
  const canteenUrl = urlService.getCanteenUrl(canteen)
  router.replace({
    name: "DashboardManager",
    params: { canteenUrlComponent: canteenUrl },
  })
}

const resetForm = (name) => {
  store.notify({ message: `Groupe ${name} créé avec succès.` })
  window.scrollTo(0, 0)
  forceRerender.value++
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
        <a :href="documentation.groupesRestaurantsSatellites" target="_blank">
          Les groupes de restaurants satellites : définition et gestion
        </a>
      </li>
      <li>
        <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">
          Annuaire des entreprises pour trouver le SIREN
        </a>
      </li>
    </AppRessources>
  </section>
  <div ref="form-ref">
    <CanteenFormGroupe
      :key="forceRerender"
      :errors="errors"
      @sendForm="(payload) => saveGroup(payload)"
    />
  </div>
</template>
