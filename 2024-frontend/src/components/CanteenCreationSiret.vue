<script setup>
import { ref, reactive } from "vue"
import { verifySiret } from "@/services/canteens.js"
import CanteenCreationResult from "@/components/CanteenCreationResult.vue"

const search = ref()
const hasSelected = ref(false)
const emit = defineEmits(["select"])

/* Canteen fields */
const canteen = reactive({})
const initFields = () => {
  canteen.founded = false
  canteen.status = null
  canteen.name = null
  canteen.siret = null
  canteen.city = null
  canteen.cityInseeCode = null
  canteen.postalCode = null
  canteen.department = null
}
initFields()

const searchSiret = () => {
  verifySiret(search.value)
    .then((response) => {
      // TODO : existe déjà dont je suis gestionnaire
      // TODO : existe déjà dont je peux réclamer
      // TODO : existe déjà dont déjà autre gestionnaire
      console.log("resposne", response)
      canteen.founded = true
      saveCanteenInfos(response)
    })
    .catch((e) => {
      console.log("error", e) // TODO
    })
}

const saveCanteenInfos = (response) => {
  canteen.status = "can-be-created"
  canteen.name = response.name
  canteen.siret = response.siret
  canteen.city = response.city
  canteen.cityInseeCode = response.cityInseeCode
  canteen.postalCode = response.postalCode
  canteen.department = response.postalCode.slice(0, 2)
}

const selectCanteen = () => {
  hasSelected.value = true
  canteen.status = "selected"
  emit("select", canteen)
}

const newSearch = () => {
  hasSelected.value = false
  search.value = ""
  initFields()
  emit("select", canteen)
}
</script>

<template>
  <div class="canteen-creation-siret">
    <p class="fr-mb-0">Mon établissement</p>
    <p class="fr-hint-text">
      Nous utilisons le site
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">annuaire-des-entreprises</a>
      afin de retrouver les informations votre établissement
    </p>
    <DsfrSearchBar
      v-if="!hasSelected"
      v-model="search"
      placeholder="Tapez votre n° SIRET"
      button-text="Rechercher"
      :large="true"
      @search="searchSiret()"
      class="fr-mb-2w"
    />
    <CanteenCreationResult
      v-if="canteen.founded"
      :name="canteen.name"
      :siret="canteen.siret"
      :city="canteen.city"
      :department="canteen.department"
      :status="canteen.status"
      @select="selectCanteen()"
    />
    <DsfrButton
      v-if="hasSelected"
      tertiary
      label="Rechercher un nouvel établissement"
      icon="fr-icon-search-line"
      icon-right
      class="canteen-creation-siret__back fr-mt-1w"
      @click="newSearch()"
    />
  </div>
</template>

<style lang="scss">
.canteen-creation-siret {
  &__back {
    width: 100%;
    justify-content: center;
  }
}
</style>
