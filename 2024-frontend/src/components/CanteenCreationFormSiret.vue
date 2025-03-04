<script setup>
import { ref, reactive } from "vue"
import { verifySiret } from "@/services/canteens.js"

const search = ref()
const canteen = reactive({})

const searchSiret = () => {
  verifySiret(search.value)
    .then((response) => {
      // TODO : existe déjà dont je suis gestionnaire
      // TODO : existe déjà dont je peux réclamer
      // TODO : existe déjà dont déjà autre gestionnaire
      console.log("resposne", response)
      canteen.founded = true
      canteen.status = "can-be-created"
      canteen.name = response.name
      canteen.siret = response.siret
      canteen.city = response.city
      canteen.cityInseeCode = response.cityInseeCode
      canteen.postalCode = response.postalCode
      canteen.department = response.postalCode.slice(0, 2)
    })
    .catch((e) => {
      console.log("error", e) // TODO
    })
}
</script>

<template>
  <div>
    <p class="fr-mb-0">Mon établissement</p>
    <p class="fr-hint-text">
      Nous utilisons le site
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">annuaire-des-entreprises</a>
      afin de retrouver les informations votre établissement
    </p>
    <DsfrSearchBar
      v-model="search"
      placeholder="Tapez votre n° SIRET"
      button-text="Rechercher"
      :large="true"
      @search="searchSiret()"
      class="fr-mb-2w"
    />
    <div v-if="canteen.founded" class="fr-card fr-p-3v">
      <div class="fr-grid-row fr-grid-row--top fr-grid-row--left fr-mb-1w">
        <p class="fr-h6 fr-mb-0 fr-col-5">{{ canteen.name }}</p>
        <div class="fr-col-offset-1"></div>
        <ul class="ma-cantine--unstyled-list fr-my-0 fr-col-6">
          <li>
            <p class="fr-mb-0 fr-text--xs">SIRET: {{ canteen.siret }}</p>
          </li>
          <li>
            <p class="fr-mb-0 fr-text--xs">Ville: {{ canteen.city }} ({{ canteen.department }})</p>
          </li>
        </ul>
      </div>
      <div v-if="canteen.status === 'can-be-created'" class="fr-grid-row fr-grid-row--center">
        <DsfrButton label="Sélectionner cet établissement" icon="fr-icon-add-circle-fill" secondary />
      </div>
    </div>
  </div>
</template>
