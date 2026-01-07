<script setup>
import { ref, reactive, computed } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens.js"

/* Setup */
defineProps(["open"])
const emit = defineEmits(["close"])
const store = useRootStore()

/* Close */
const closeModal = () => {
  emit("close")
  hasSiret.value = ''
  resetSearch()
}

/* Checkboxes */
const hasSiret = ref('')
const radioOptions = [
  {
    label: 'Oui',
    value: 'oui',
  },
  {
    label: 'Non',
    value: 'non',
  },
]

/* Search */
const search = ref('')
const errorNotFound = ref('')
const numberName = computed(() => hasSiret.value === 'oui' ? "SIRET" : "SIREN")
const canteen = reactive({})

const resetSearch = () => {
  search.value = ''
  errorNotFound.value = ''
  canteen.found = false
}

const searchByNumber = () => {
  const cleanNumber = search.value.replaceAll(" ", "")
  if (cleanNumber.length === 0) return
  const searchBy = numberName.value.toLowerCase()
  canteensService
    .canteenStatus(searchBy, cleanNumber)
    .then((response) => {
      const noCanteenSiretFound = !response.id && !response.siren
      const noCanteenSirenFound = !response.id && response.siren && response.canteens.length === 0
      switch (true) {
        case response instanceof Error:
          canteen.found = false
          errorNotFound.value = "Une erreur est survenue lors de la recherche de l'établissement, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr"
          break
        case response.length === 0:
          canteen.found = false
          errorNotFound.value = `D’après l'annuaire-des-entreprises le numéro ${numberName.value} « ${cleanNumber} » ne correspond à aucun établissement`
          break
        case noCanteenSiretFound || noCanteenSirenFound:
          canteen.found = false
          errorNotFound.value = `Aucune cantine enregistrée avec le numéro ${numberName.value} « ${cleanNumber} » sur la plateforme`
          break
        // TODO : n'est pas une SAT
        // TODO : est déjà rattaché à un groupe
        // TODO : est rattachable à mon groupe
      }
    })
    .catch((e) => store.notifyServerError(e))
}
</script>
<template>
  <DsfrModal :opened="open" title="Ajouter un restaurant satellite" @close="closeModal()" size="lg">
    <p>Pour ajouter une cantine à votre groupe cette dernière doit : être enregistrée sur la plateforme, être de type "Restaurant satellite", ne doit pas déjà être associée à un groupe.</p>
    <DsfrRadioButtonSet
      v-model="hasSiret"
      @change="resetSearch"
      legend="Le restaurant satellite a-t-il un numéro SIRET ?"
      :options="radioOptions"
      name="hasSiret"
      small
      inline
    />
    <DsfrInputGroup :error-message="errorNotFound">
      <template #default>
        <DsfrSearchBar
          v-if="hasSiret"
          v-model="search"
          button-text="Rechercher"
          :placeholder="`Tapez le n° ${numberName} du restaurant satellite`"
          @search="searchByNumber"
          large
        />
      </template>
    </DsfrInputGroup>
  </DsfrModal>
</template>
