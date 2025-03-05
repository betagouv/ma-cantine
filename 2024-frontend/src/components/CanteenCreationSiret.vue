<script setup>
import { ref, reactive } from "vue"
import canteensService from "@/services/canteens.js"
import CanteenCreationResult from "@/components/CanteenCreationResult.vue"

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

/* Search */
const search = ref()
const hasSelected = ref(false)
const searchSiret = () => {
  canteensService
    .verifySiret(search.value)
    .then((response) => {
      console.log("resposne", response)
      switch (true) {
        case !response.id:
          canteen.status = "can-be-created"
          canteen.founded = true
          break
        case response.isManagedByUser:
          canteen.founded = true
          canteen.status = "managed-by-user"
          break
        case response.canBeClaimed:
          canteen.founded = true
          canteen.status = "can-be-claimed"
          break
        case !response.canBeClaimed:
          canteen.founded = true
          canteen.status = "ask-to-join"
          break
      }
      // TODO : établissement non trouvé

      saveCanteenInfos(response)
    })
    .catch((e) => {
      console.log("error", e) // TODO
    })
}

const saveCanteenInfos = (response) => {
  canteen.id = response.id
  canteen.name = response.name
  canteen.siret = response.siret
  canteen.city = response.city
  canteen.cityInseeCode = response.cityInseeCode
  canteen.postalCode = response.postalCode
  canteen.department = response.postalCode.slice(0, 2)
}

/* Select canteen */
const emit = defineEmits(["select"])
const selectCanteen = () => {
  hasSelected.value = true
  canteen.status = "selected"
  emit("select", canteen)
}
const unselectCanteen = () => {
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
      :id="canteen.id"
      @select="selectCanteen()"
    />
    <DsfrButton
      v-if="hasSelected"
      tertiary
      label="Rechercher un nouvel établissement"
      icon="fr-icon-search-line"
      icon-right
      class="canteen-creation-siret__back fr-mt-1w"
      @click="unselectCanteen()"
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
