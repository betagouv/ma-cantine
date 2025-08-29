<script setup>
import { ref, reactive, computed } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens.js"
import CanteenEstablishmentCard from "@/components/CanteenEstablishmentCard.vue"

/* Props */
const props = defineProps(["errorRequired"])
const store = useRootStore()
const hasSelected = ref(false)
const centralProductionTypes = ['central', 'central_serving']

/* Canteen fields */
const canteen = reactive({})
const initFields = () => {
  canteen.found = false
  canteen.status = null
  canteen.name = null
  canteen.siret = null
  canteen.city = null
  canteen.department = null
}
initFields()

/* Search */
const search = ref("")
const errorNotFound = ref()
const errorMessage = computed(() => {
  if (errorNotFound.value) return errorNotFound.value
  if (props.errorRequired && !canteen.found) return props.errorRequired
  if (props.errorRequired && canteen.found) return "Vous devez sélectionner un établissement"
  else return ""
})
const searchByNumber = () => {
  const cleanNumber = search.value.replaceAll(" ", "")
  if (cleanNumber.length === 0) return
  initFields()
  errorNotFound.value = ""
  canteensService
    .canteenStatus('siret', cleanNumber)
    .then((response) => {
      switch (true) {
        case response.length === 0:
          canteen.found = false
          errorNotFound.value = `D’après l'annuaire-des-entreprises le numéro SIRET « ${cleanNumber} » ne correspond à aucun établissement`
          break
        case !response.id :
          canteen.found = false
          errorNotFound.value = `Le livreur de repas avec le numéro SIRET « ${cleanNumber} » n’est pas encore inscrit sur la plateforme, veuillez vous rapprocher de cet établissement pour aller plus loin`
          break
        case response.id && !centralProductionTypes.includes(response.productionType):
          canteen.found = false
          errorNotFound.value = `L'établissement avec le numéro SIRET « ${cleanNumber} » n’est pas enregistré comme livreur de repas sur la plateforme, veuillez vous rapprocher de cet établissement pour aller plus loin`
          break
        case response.id && centralProductionTypes.includes(response.productionType):
          canteen.found = true
          canteen.status = "can-be-central"
          break
      }
      if (canteen.found) saveCanteenInfos(response)
    })
    .catch((e) => store.notifyServerError(e))
}

const saveCanteenInfos = (response) => {
  canteen.name = response.name
  canteen.siret = response.siret
  canteen.city = response.city
  canteen.department = response.department
}

/* Select canteen */
const emit = defineEmits(["select"])
const selectCanteen = () => {
  hasSelected.value = true
  canteen.status = "selected"
  emit("select", canteen.siret)
}
const unselectCanteen = () => {
  hasSelected.value = false
  search.value = ""
  initFields()
  emit("select", "")
}
</script>

<template>
  <div class="canteen-establishment-search">
    <p class="fr-mb-0">SIRET du livreur *</p>
    <p class="fr-hint-text">
      Vous ne le connaissez pas ? Trouvez-le avec
      <a href="https://annuaire-entreprises.data.gouv.fr/" target="_blank">l'annuaire-des-entreprises</a>
    </p>
    <DsfrInputGroup :error-message="errorMessage">
      <template #default>
        <DsfrSearchBar
          v-if="!hasSelected"
          v-model="search"
          button-text="Rechercher"
          placeholder="Tapez le n° SIRET du livreur"
          label="Rechercher un livreur par son numéro SIRET"
          :large="true"
          @search="searchByNumber()"
        />
      </template>
    </DsfrInputGroup>
    <CanteenEstablishmentCard
      v-if="canteen.found"
      :name="canteen.name"
      :siret="canteen.siret"
      :status="canteen.status"
      :city="canteen.city"
      :department="canteen.department"
      @select="selectCanteen()"
    />
    <p v-if="canteen.found && !hasSelected" class="fr-text--xs fr-mb-0 fr-mt-1w ma-cantine--text-center">
      Ce n’est pas le bon établissement ? Refaites une recherche via le bon numéro SIRET, ou trouvez
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
