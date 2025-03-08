<script setup>
import { ref, reactive } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens.js"
import CanteenCreationResult from "@/components/CanteenCreationResult.vue"

/* Props */
defineProps(["error"])

/* Store */
const store = useRootStore()

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
const showEmptyResult = ref(false)
const hasSearched = ref(false)
const hasSelected = ref(false)
const searchSiret = () => {
  const cleanSiret = search.value.replaceAll(" ", "")
  if (cleanSiret.length === 0) return
  hasSearched.value = true
  canteensService
    .verifySiret(cleanSiret)
    .then((response) => {
      switch (true) {
        case response.length === 0:
          canteen.founded = false
          showEmptyResult.value = true
          break
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
      if (canteen.founded) saveCanteenInfos(response)
    })
    .catch((e) => store.notifyServerError(e))
}

const verifyIfEmtpy = () => {
  if (search.value.length === 0 && hasSearched.value) showEmptyResult.value = false
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
  hasSearched.value = false
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
      afin de retrouver les informations de votre établissement
    </p>
    <DsfrInputGroup :error-message="error">
      <template #default>
        <DsfrSearchBar
          v-if="!hasSelected"
          v-model="search"
          placeholder="Tapez votre n° SIRET"
          button-text="Rechercher"
          label="Rechercher un établissement par son numéro SIRET"
          :large="true"
          @update:modelValue="verifyIfEmtpy()"
          @search="searchSiret()"
        />
      </template>
    </DsfrInputGroup>
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
    <p v-if="canteen.founded && !hasSelected" class="fr-text--xs fr-mb-0 fr-mt-1w ma-cantine--text-center">
      Ce n’est pas le bon établissement ? Refaites une recherche via le bon numéro SIRET, ou trouvez l’information dans
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
    </p>
    <p v-if="showEmptyResult" class="fr-text--xs fr-mb-0 ma-cantine--text-center">
      D’après
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
      <br />
      le numéro SIRET "{{ search }}" ne correspond à aucun établissement
    </p>
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
