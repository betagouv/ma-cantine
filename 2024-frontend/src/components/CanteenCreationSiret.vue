<script setup>
import { ref, reactive } from "vue"
import { verifySiret } from "@/services/canteens.js"
import CanteenCreationCard from "@/components/CanteenCreationCard.vue"

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
    <pre>{{ 91100348100015 }}</pre>
    <DsfrSearchBar
      v-model="search"
      placeholder="Tapez votre n° SIRET"
      button-text="Rechercher"
      :large="true"
      @search="searchSiret()"
      class="fr-mb-2w"
    />
    <CanteenCreationCard
      v-if="canteen.founded"
      :name="canteen.name"
      :siret="canteen.siret"
      :city="canteen.city"
      :department="canteen.department"
      :status="canteen.status"
    />
  </div>
</template>
