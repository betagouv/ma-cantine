<script setup>
import { ref, computed } from "vue"
import { useRootStore } from "@/stores/root"
import canteensService from "@/services/canteens.js"
import CanteenEstablishmentCard from "@/components/CanteenEstablishmentCard.vue"

/* Setup */
const props = defineProps(["open", "groupId"])
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
const canteens = ref([])

const resetSearch = () => {
  search.value = ''
  errorNotFound.value = ''
  canteens.value = []
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
      let hasCanteen = false
      switch (true) {
        case response instanceof Error:
          hasCanteen = false
          errorNotFound.value = "Une erreur est survenue lors de la recherche de l'établissement, vous pouvez réessayer plus tard ou nous contacter directement à support-egalim@beta.gouv.fr"
          break
        case response.length === 0:
          hasCanteen = false
          errorNotFound.value = `D’après l'annuaire-des-entreprises le numéro ${numberName.value} « ${cleanNumber} » ne correspond à aucun établissement`
          break
        case noCanteenSiretFound || noCanteenSirenFound:
          hasCanteen = false
          errorNotFound.value = `Aucune cantine enregistrée avec le numéro ${numberName.value} « ${cleanNumber} » sur la plateforme`
          break
        default:
          hasCanteen = true
      }
      if (hasCanteen) updateCanteenResult(response)
    })
    .catch((e) => store.notifyServerError(e))
}

const updateCanteenResult = (response) => {
  let list = []
  const canteensInfo = response.siret ? [response] : response.canteens
  for (const canteen of canteensInfo) list.push(getCanteenInfos(canteen))
  canteens.value = list
}

const getCanteenInfos = (canteen) => {
  const infos = {
    id: canteen.id,
    name: canteen.name,
    city: canteen.city,
    department: canteen.department,
    status: getCanteenStatus(canteen),
  }
  if (canteen.siren) infos.siren = canteen.siren
  if (canteen.siret) infos.siret = canteen.siret
  return infos
}

const getCanteenStatus = (canteen) => {
  const isSatellite = canteen.productionType === "site_cooked_elsewhere"
  const hasGroup = canteen.groupe !== null
  const inMyGroup = hasGroup && canteen.groupe== props.groupId
  if (!isSatellite) return "not-a-satellite"
  if (isSatellite && !hasGroup) return "add-satellite"
  if (isSatellite && hasGroup && inMyGroup) return "my-group"
  if (isSatellite && hasGroup && !inMyGroup) return "other-group"
  return ""
}

const addSatellite = (canteen) => {
  console.log('addSatellite', canteen)
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
    <ul v-if="canteens.length > 0" class="ma-cantine--unstyled-list">
      <li class="fr-mb-1w" v-for="canteen in canteens" :key="canteen.id">
        <CanteenEstablishmentCard
          :name="canteen.name"
          :siret="canteen.siret"
          :siren="canteen.siren"
          :city="canteen.city"
          :department="canteen.department"
          :status="canteen.status"
          :id="canteen.id"
          :linked-canteens="canteen.linkedCanteens"
          @select="addSatellite(canteen)"
        />
      </li>
    </ul>
  </DsfrModal>
</template>
