<script setup>
import { ref } from "vue"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root.js"
import { useStoreTeledeclaration } from "@/stores/teledeclaration.js"
import diagnosticService from "@/services/diagnostics.js"

defineProps(["opened"])
const emit = defineEmits(["close"])

const router = useRouter()
const rootStore = useRootStore()
const teledeclarationStore = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(teledeclarationStore)
const loading = ref(false)

const cancelTeledeclaration = () => {
  if (!diagnostic.value) return
  loading.value = true
  diagnosticService
    .cancelTeledeclaration(diagnostic.value.canteenId, diagnostic.value.id)
    .then((response) => {
      if (response?.status === "error" || response instanceof Error) rootStore.notifyServerError(response)
      else {
        teledeclarationStore.setDiagnostic({ ...diagnostic.value, isTeledeclared: false })
        router.push({ name: "GestionnaireTunnelApproInformations" })
      }
    })
    .catch((e) => rootStore.notifyServerError(e))
    .finally(() => {
      loading.value = false
    })
}
</script>

<template>
  <DsfrModal
    :opened="opened"
    title="Modifier ma déclaration"
    icon="fr-icon-edit-line"
    @close="emit('close')"
  >
    <p class="fr-h6">Attention : toute modification nécessite une nouvelle déclaration.</p>
    <div class="fr-mb-3w">
      Si vous modifiez les informations de votre déclaration, son statut repassera automatiquement à
      <DsfrBadge label="À télédéclarer" type="warning" no-icon small />.
      Une fois vos modifications terminées, pensez à cliquer de nouveau sur le bouton « Valider ma télédéclaration » afin que vos nouvelles données soient prises en compte.
    </div>
    <div class="fr-mb-3w">
      Votre cantine repassera alors au statut
      <DsfrBadge label="Télédéclaré" type="success" small />,
      vous permettant d’être en conformité avec la réglementation et d’accéder à votre justificatif de déclaration.
    </div>
    <p class="fr-text--bold">Souhaitez-vous poursuivre les modifications ?</p>
    <div class="ma-cantine--flex-end">
      <DsfrButton
        secondary
        label="Annuler"
        :disabled="loading"
        @click="emit('close')"
      />
      <DsfrButton
        primary
        label="Oui, je confirme"
        :disabled="loading"
        @click="cancelTeledeclaration"
      />
    </div>
  </DsfrModal>
</template>
