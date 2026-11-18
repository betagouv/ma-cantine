<script setup>
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary"
import { storeToRefs } from "pinia"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import DiagnosticEgalimSimple from "@/components/DiagnosticEgalimSimple.vue"
import DiagnosticEgalimComplete from "@/components/DiagnosticEgalimComplete.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import IconOSAMonochrome from "@/components/IconOSAMonochrome.vue"
import TunnelTeledeclarationUPSABanner from "@/components/TunnelTeledeclarationUPSABanner.vue"
import TunnelTeledeclarationMealCostField from "@/components/TunnelTeledeclarationMealCostField.vue"
import AppFormMentionOptionalFields from "@/components/AppFormMentionOptionalFields.vue"
import tunnelTeledeclarationService from "@/services/tunnelTeledeclaration.js"

/* Fields names */
const valeurTotalFieldName = tunnelTeledeclarationService.getFieldsListFromGroup("valeurTotale")[0]
const onChangeTotalField = async () => await storeTeledeclaration.saveMealCost()

/* Teledeclaration */
const storeTeledeclaration = useStoreTeledeclaration()
const { isSimple, isComplete } = storeToRefs(storeTeledeclaration)

/* Purchases */
const storePurchaseSummary = useStorePurchaseSummary()
const { hasPurchaseTotal } = storeToRefs(storePurchaseSummary)
</script>
<template>
  <TunnelTeledeclarationUPSABanner />
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Approvisionnements EGalim</h2>
      <p class="fr-mb-0">
        Cette étape du volet « Approvisionnements » de la télédéclaration est obligatoire. Vous y renseignez vos achats au regard des 12 catégories EGalim.
      </p>
      <p v-if="isSimple" class="fr-mt-2w fr-mb-0">
        En saisie simplifiée, ces 12 catégories sont regroupées en quatre groupes (bio, SIQO (hors bio), autres EGalim, critères d'achats (pour les marchés publics)).
      </p>
      <AppFormMentionOptionalFields class="fr-mt-2w fr-mb-0" />
      <div v-if="hasPurchaseTotal" class="ma-cantine--flex-between ma-cantine--flex-top ma-cantine--flex-gap-1 fr-mt-4w">
        <DsfrTag small class="ma-cantine--tag-blue ma-cantine--width-2w fr-mt-1v">
          <IconOSAMonochrome />
        </DsfrTag>
        <p class="ma-cantine--flex-grow fr-mb-0">
          Outil Suivi des Achats : vous pouvez remplir les champs automatiquement à partir des achats que vous avez saisis
        </p>
      </div>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur les 12 catégories EGalim">
        <ul class="ma-cantine--unstyled-list fr-mb-0">
          <li class="fr-mb-1w">
            <a :href="`${documentation.qualiteDurabiliteProduits}/#1-les-12-categories-egalim`" target="_blank">Les 12 catégories</a>
          </li>
          <li v-if="isSimple" class="fr-mb-1w">
            <a :href="documentation.teledeclarationMatriceSimplifiee" target="_blank">Matrice</a>
          </li>
          <li v-else-if="isComplete" class="fr-mb-1w">
            <a :href="documentation.teledeclarationMatriceDetaillee" target="_blank">Matrice</a>
          </li>
          <li v-if="isSimple" class="fr-mb-1w">
            <a :href="documentation.teledeclarationAntisecheSimplifiee" target="_blank">Antisèche</a>
          </li>
          <li v-else-if="isComplete" class="fr-mb-1w">
            <a :href="documentation.teledeclarationAntisecheDetaillee" target="_blank">Antisèche</a>
          </li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-mb-6w">
    <h3 class="fr-h5">Total des achats</h3>
    <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top">
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationField :name="valeurTotalFieldName" @change="onChangeTotalField" />
      </div>
      <div class="fr-col-12 fr-col-md-6">
        <TunnelTeledeclarationMealCostField class="fr-mb-0" />
      </div>
    </div>
  </div>
  <DiagnosticEgalimSimple v-if="isSimple" />
  <DiagnosticEgalimComplete v-else-if="isComplete" />
  <DsfrAlert v-else type="warning">
    <p>
      Pour renseigner le détail de vos achats EGalim vous devez sélectionner
      <AppLinkRouter :to="{name: 'GestionnaireTunnelApproSaisie'}" title="un mode de saisie" />.
    </p>
  </DsfrAlert>
</template>
