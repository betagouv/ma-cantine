<script setup>
import { ref, computed } from "vue"
import { useRouter, useRoute } from "vue-router"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import { useStoreCanteen } from "@/stores/canteen.js"
import { storeToRefs } from "pinia"
import canteenServices from "@/services/canteens"
import diagnosticServices from "@/services/diagnostics"
import diagnosticsFields from "@/services/diagnosticsFields"
import AppErrorList from "@/components/AppErrorList.vue"

const router = useRouter()
const route = useRoute()
const diagnosticStore = useStoreDiagnostic()
const canteenStore = useStoreCanteen()
const previousStep = computed(() => route.meta.previous)
const nextStep = computed(() => route.meta.next)
const { canteenInformations } = storeToRefs(canteenStore)
const { diagnosticCurrentCampaign, diagnosticCurrentCampaignErrors } = storeToRefs(diagnosticStore)

/* Save */
const save = async (page) => {
  diagnosticStore.clearDiagnosticCurrentCampaignErrors()
  await diagnosticStore.saveDiagnosticCurrentCampaign()
  const check = await checkIsFilled()
  if (check.isFilled) goTo(page)
  await saveErrors(check.errors)
  const pageErrors = filterErrorsOnPage()
  if (pageErrors.length > 0) displayModal(pageErrors, page)
  else goTo(page)
}

const saveAndQuit = async () => {
  await diagnosticStore.saveDiagnosticCurrentCampaign()
  router.push({ name: 'GestionnaireCantineTeledeclarationEnCours' })
}

/* Errors */
const saveErrors = async (errors) => {
  const errorsKeys = Object.keys(errors)
  const errorsValues = Object.values(errors)
  const errorList = []
  for (let i = 0; i < errorsKeys.length; i++) {
    errorList.push({ field: errorsKeys[i], message: errorsValues[i] })
  }
  await diagnosticStore.saveDiagnosticCurrentCampaignErrors(errorList)
}

const checkIsFilled = async () => {
  const canteenId = diagnosticCurrentCampaign.value.canteenId
  const diagnosticId = diagnosticCurrentCampaign.value.id
  const checkCanteen = await canteenServices.checkCanteen(canteenId)
  const checkDiagnostic = await diagnosticServices.checkDiagnostic(canteenId, diagnosticId)
  return { isFilled: checkCanteen.isFilled && checkDiagnostic.isFilled, errors: {...checkCanteen.errors, ...checkDiagnostic.errors} }
}

const filterErrorsOnPage = () => {
  const pageName = route.name
  const canteenIsGroupe = canteenInformations.value.isGroupe
  const diagnosticIsSimple = diagnosticCurrentCampaign.value.diagnosticType === "SIMPLE"
  const fieldsList = diagnosticsFields.getFieldsList(pageName, canteenIsGroupe, diagnosticIsSimple)
  return diagnosticCurrentCampaignErrors.value.filter(error => fieldsList.includes(error.field))
}


/* Modal */
const showModal = ref(false)
const modalTitle = ref("")
const modalLink = ref("")
const modalErrors = ref([])
const displayModal = (errors, page) => {
  showModal.value = true
  modalErrors.value = errors
  modalTitle.value = errors.length > 1 ? "Erreurs détectées" : "Erreur détectée"
  modalLink.value = page
}

/* Redirect */
const goTo = (page) => {
  showModal.value = false
  router.push({ name: page })
}
</script>

<template>
  <nav class="tunnel-teledeclaration-top-nav ma-cantine--sticky__top fr-background-default--grey fr-py-2w">
    <DsfrButton
      tertiary
      icon="fr-icon-save-line"
      label="Enregistrer et finir plus tard"
      no-outline
      @click="saveAndQuit()"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-left-s-first-line"
      label="Étape précédente"
      @click="save(previousStep)"
      :disabled="!previousStep"
    />
    <DsfrButton
      secondary
      icon="fr-icon-arrow-right-s-last-line"
      label="Étape suivante"
      @click="save(nextStep)"
      :disabled="!nextStep"
      :icon-right="true"
    />
  </nav>
  <DsfrModal
    :opened="showModal"
    :title="modalTitle"
    @close="showModal = false"
  >
    <p>Après l'enregistrement de vos données, nous avons détecté une ou plusieurs erreurs : </p>
    <AppErrorList :errors="modalErrors.map((error) => error.field)" />
    <p>Vous n'êtes pas obligé de faire la correction maintenant mais vous devrez la faire avant de télédéclarer.</p>
    <div class="ma-cantine--flex-end">
      <DsfrButton
        secondary
        icon="fr-icon-edit-line"
        label="Revenir et corriger"
        @click="showModal = false"
        :icon-right="true"
      />
      <DsfrButton
        primary
        label="Continuer et corriger plus tard"
        @click="goTo(modalLink)"
      />
    </div>
  </DsfrModal>
</template>

<style lang="scss" scoped>
.tunnel-teledeclaration-top-nav {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 1rem;
}
</style>
