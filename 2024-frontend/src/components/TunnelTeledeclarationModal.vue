<script setup>
import { computed, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useRootStore } from '@/stores/root'
import { useStoreTeledeclaration } from '@/stores/teledeclaration'
import { useStoreCanteen } from '@/stores/canteen'

const opened = defineModel(['opened'])
const emit = defineEmits(['close'])
const rootStore = useRootStore()
const router = useRouter()

/* Teledeclaration */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)

/* Canteen */
const storeCanteen = useStoreCanteen()
const { canteenInformations } = storeToRefs(storeCanteen)
const isGroupe = computed(() => canteenInformations.value?.isGroupe)
const title = computed(() => {
  if (!isGroupe.value) return 'Plus qu’une étape pour valider votre télédéclaration'
  const count = canteenInformations.value.satellitesCount
  const restaurants = count > 1 ? `vos ${count} restaurants` : 'votre restaurant'
  return `Plus qu’une étape pour télédéclarer ${restaurants}`
})

/* Modale */
const checkBoxeConfirmed = ref(false)
const checkBoxeCgu = ref(false)
const loading = ref(false)
const modalActions = computed(() => [
  {
    label: loading.value ? 'Télédéclaration en cours...' : 'Télédéclarer ces données',
    icon: 'ri-send-plane-line',
    disabled: !checkBoxeConfirmed.value || !checkBoxeCgu.value || loading.value,
    onClick: teledeclare,
  },
  {
    label: 'Annuler',
    secondary: true,
    onClick: closeModal,
  },
])

const closeModal = () => {
  checkBoxeConfirmed.value = false
  checkBoxeCgu.value = false
  loading.value = false
  emit('close')
}

/* Teledeclare */
const teledeclare = () => {
  if (!diagnostic.value) return
  loading.value = true
  storeTeledeclaration
    .teledeclare()
    .then((response) => {
      if (response?.status === 'error' || response instanceof Error) displayError(response)
      else {
        router.push({ name: 'GestionnaireTunnelApproTeledeclares' })
      }
    })
    .catch((e) =>  displayError(e))
    .finally(() => {
      loading.value = false
    })
}

const displayError = (error) => {
  rootStore.notifyServerError(error)
  loading.value = false
}
</script>

<template>
  <DsfrModal
    :opened="opened"
    :title="title"
    @close="closeModal"
    :actions="modalActions"
  >
    <p v-if="isGroupe">
      Vous allez effectuer une déclaration pour l’ensemble des cantines de votre groupe. Les cantines de votre groupe pourront ajouter des approvisionnements additionnels et compléter les volets thématiques.
    </p>
    <p>
      Une fois votre télédéclaration effectuée, votre télédéclaration reste modifiable jusqu’à la fin de la campagne de correction.
    </p>
    <p>
      Retrouver votre justificatif de déclaration et la synthèse de votre qualité de produits dans la page de votre {{ isGroupe ? 'groupe' : 'cantine' }}.
    </p>
    <DsfrCheckbox
      v-model="checkBoxeConfirmed"
      name="checkBoxeConfirmed"
      label="Je déclare sur l'honneur la véracité de ces informations"
    />
    <DsfrCheckbox
      v-model="checkBoxeCgu"
      name="checkBoxeCgu"
      label="J’ai lu et j’accepte les Conditions Générales d’Utilisation de mes données"
    >
      <template #label>
        J’ai lu et j’accepte les
        <router-link :to="{ name: 'ConditionsGeneralesUtilisation' }" target="_blank">Conditions Générales d’Utilisation de mes données</router-link>
      </template>
    </DsfrCheckbox>
  </DsfrModal>
</template>
