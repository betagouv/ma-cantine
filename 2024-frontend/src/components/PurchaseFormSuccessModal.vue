<script setup>
import { useRouter, useRoute } from "vue-router"
import urlService from "@/services/urls.js"

const props = defineProps(["purchaseId"])
const emit = defineEmits(["close"])
const router = useRouter()
const route = useRoute()
const canteenName = urlService.getCanteenName(route.params.canteenUrlComponent)
const canteenUrlComponent = route.params.canteenUrlComponent

/* Actions */
const goToAddInvoice = () => {
  router.push({ name: "GestionnaireAchatsModifier", params: { id: props.purchaseId, canteenUrlComponent: canteenUrlComponent } })
}

const goToPurchasesList = () => {
  router.push({ name: "PurchasesHome" })
}

/* Close */
const closeModal = () => {
  emit("close")
}
</script>
<template>
  <DsfrModal
    :opened="true"
    icon="fr-icon-checkbox-circle-fill"
    title="Achat enregistré"
    @close="closeModal"
    :actions="[
      {
        label: 'Voir tous mes achats',
        onClick: goToPurchasesList,
      },
      {
        label: 'Ajouter un nouvel achat',
        secondary: true,
        onClick: closeModal,
      },
    ]"
  >
    <p>L'achat a bien été enregistré pour la cantine « {{ canteenName }} ».</p>
    <DsfrHighlight class="fr-ml-0">
      <p>Si vous souhaitez ajouter une facture à cet achat, vous pouvez le faire en cliquant sur le bouton ci-dessous. Ce champ est facultatif, il n'est pas nécessaire d'importer ses factures pdf si vous disposez déjà d'un espace de stockage fiable et sécurisé (sur votre ordinateur ou autre logiciel par exemple).</p>
      <DsfrButton
        label="Ajouter la facture de mon achat"
        tertiary
        icon="fr-icon-file-add-line"
        @click="goToAddInvoice"
        size="small"
      />
    </DsfrHighlight>
  </DsfrModal>
</template>
