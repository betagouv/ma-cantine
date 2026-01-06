<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
import AppRessources from "@/components/AppRessources.vue"
import CanteenGroupForm from "@/components/CanteenGroupForm.vue"

/* Router and Store */
const route = useRoute()

/* Component */
const forceRerender = ref(0)

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
  <CanteenGroupForm
    :key="forceRerender"
    @sendForm="(payload) => saveGroup(payload)"
  />
</template>
