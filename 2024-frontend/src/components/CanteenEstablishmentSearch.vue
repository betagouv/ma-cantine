<script setup>
import { ref, reactive, computed } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens.js"
import CanteenEstablishmentCard from "@/components/CanteenEstablishmentCard.vue"

/* Props */
const props = defineProps(["searchName", "label", "placeholder", "errorRequired", "establishmentData"])
const store = useRootStore()
const hasSelected = ref(false)

/* Canteen fields */
const canteen = reactive({})
const initFields = () => {
  canteen.found = false
  canteen.status = null
  canteen.name = null
  canteen.siret = null
  canteen.city = null
  canteen.cityInseeCode = null
  canteen.postalCode = null
  canteen.department = null
  canteen.linkedCanteens = []
  canteen.siren = null
}
const prefillFields = () => {
  hasSelected.value = true
  canteen.found = true
  canteen.status = "selected"
  canteen.siren = props.establishmentData.sirenUniteLegale
  canteen.siret = props.establishmentData.siret
  canteen.city = props.establishmentData.city
  canteen.department = props.establishmentData.department
  canteen.name = props.establishmentData.name
}

if (props.establishmentData) prefillFields()
else initFields()

/* Search */
const search = ref("")
const errorNotFound = ref("")
const errorMessage = computed(() => {
  if (errorNotFound.value) return errorNotFound.value
  if (props.errorRequired && !canteen.found) return props.errorRequired
  if (props.errorRequired && canteen.found) return "Vous devez sélectionner un établissement dans la liste ci-dessous"
  return ""
})
const searchByNumber = () => {
  const cleanNumber = search.value.replaceAll(" ", "")
  if (cleanNumber.length === 0) return
  initFields()
  errorNotFound.value = ""
  const searchBy = props.searchName.toLowerCase()
  canteensService
    .canteenStatus(searchBy, cleanNumber)
    .then((response) => {
      switch (true) {
        case response.length === 0:
          canteen.found = false
          errorNotFound.value = `D’après l'annuaire-des-entreprises le numéro ${props.searchName} « ${cleanNumber} » ne correspond à aucun établissement`
          break
        case !response.id && !response.siren:
          canteen.found = true
          canteen.status = "can-be-created"
          break
        case !response.id && response.siren !== "":
          canteen.found = true
          canteen.status = "can-be-linked"
          break
        case response.isManagedByUser:
          canteen.found = true
          canteen.status = "managed-by-user"
          break
        case response.canBeClaimed:
          canteen.found = true
          canteen.status = "can-be-claimed"
          break
        case !response.canBeClaimed:
          canteen.found = true
          canteen.status = "ask-to-join"
          break
      }
      if (canteen.found) saveCanteenInfos(response)
    })
    .catch((e) => store.notifyServerError(e))
}

const saveCanteenInfos = (response) => {
  canteen.id = response.id
  canteen.name = response.name
  canteen.siret = response.siret
  canteen.city = response.city
  canteen.cityInseeCode = response.cityInseeCode
  canteen.postalCode = response.postalCode
  canteen.department = response.department
  canteen.linkedCanteens = response.canteens
  canteen.siren = response.siren
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
  <div class="canteen-establishment-search">
    <p class="fr-mb-0">{{ label }} *</p>
    <slot name="description"></slot>
    <DsfrInputGroup :error-message="errorMessage">
      <template #default>
        <DsfrSearchBar
          v-if="!hasSelected"
          v-model="search"
          button-text="Rechercher"
          :placeholder="placeholder"
          label="Rechercher un établissement"
          :large="true"
          @search="searchByNumber()"
        />
      </template>
    </DsfrInputGroup>
    <CanteenEstablishmentCard
      v-if="canteen.found"
      :name="canteen.name"
      :siret="canteen.siret"
      :siren="canteen.siren"
      :city="canteen.city"
      :department="canteen.department"
      :status="canteen.status"
      :id="canteen.id"
      :linked-canteens="canteen.linkedCanteens"
      @select="selectCanteen()"
    />
    <p v-if="canteen.found && !hasSelected" class="fr-text--xs fr-mb-0 fr-mt-1w ma-cantine--text-center">
      Ce n’est pas le bon établissement ? Refaites une recherche, ou trouvez
      l’information dans
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
    </p>
    <DsfrButton
      v-if="hasSelected"
      tertiary
      label="Rechercher un nouvel établissement"
      icon="fr-icon-search-line"
      icon-right
      class="canteen-establishment-search__back fr-mt-1w"
      @click="unselectCanteen()"
    />
  </div>
</template>

<style lang="scss">
.canteen-establishment-search {
  &__back {
    width: 100%;
    justify-content: center;
  }
}
</style>
