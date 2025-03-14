<script setup>
import { ref, reactive, computed } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens.js"
import CanteenCreationResult from "@/components/CanteenCreationResult.vue"

/* Props */
const props = defineProps(["errorRequired", "hasSiret"])

/* Store */
const store = useRootStore()

/* Content */
const numberName = computed(() => (props.hasSiret ? "SIRET" : "SIREN"))
const title = computed(() => (props.hasSiret ? "Mon établissement" : "Mon unité légale de rattachement"))
const establishment = computed(() => (props.hasSiret ? "votre établissement" : "l'établissement"))
const placeholder = computed(() => (props.hasSiret ? "Tapez votre n° SIRET" : "Tapez le n° SIREN de l’unité légale"))
const label = computed(() => `Rechercher un établissement par son numéro ${numberName.value}`)

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
const search = ref("")
const errorNotFound = ref()
const errorMessage = computed(() => {
  if (errorNotFound.value) return errorNotFound.value
  if (props.errorRequired && !canteen.founded) return props.errorRequired
  if (props.errorRequired && canteen.founded) return `Vous devez sélectionner un établissement`
  else return ""
})
const hasSelected = ref(false)
const searchByNumber = () => {
  const cleanNumber = search.value.replaceAll(" ", "")
  if (cleanNumber.length === 0) return
  errorNotFound.value = ""
  const searchBy = numberName.value.toLowerCase()
  canteensService
    .canteenStatus(searchBy, cleanNumber)
    .then((response) => {
      console.log("response", response)
      switch (true) {
        case response.length === 0:
          canteen.founded = false
          errorNotFound.value = `D’après l'annuaire-des-entreprises le numéro ${numberName.value} « ${cleanNumber} » ne correspond à aucun établissement`
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
  <div class="canteen-creation-search">
    <p class="fr-mb-0">{{ title }} *</p>
    <p class="fr-hint-text">
      Nous utilisons le site
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">annuaire-des-entreprises</a>
      afin de retrouver les informations de {{ establishment }}
    </p>
    <DsfrInputGroup :error-message="errorMessage">
      <template #default>
        <DsfrSearchBar
          v-if="!hasSelected"
          v-model="search"
          button-text="Rechercher"
          :placeholder="placeholder"
          :label="label"
          :large="true"
          @search="searchByNumber()"
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
      Ce n’est pas le bon établissement ? Refaites une recherche via le bon numéro {{ numberName }}, ou trouvez
      l’information dans
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
    </p>
    <DsfrButton
      v-if="hasSelected"
      tertiary
      label="Rechercher un nouvel établissement"
      icon="fr-icon-search-line"
      icon-right
      class="canteen-creation-search__back fr-mt-1w"
      @click="unselectCanteen()"
    />
  </div>
</template>

<style lang="scss">
.canteen-creation-search {
  &__back {
    width: 100%;
    justify-content: center;
  }
}
</style>
