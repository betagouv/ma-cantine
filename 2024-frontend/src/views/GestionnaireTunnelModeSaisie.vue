<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"
import { useStorePurchaseSummary } from "@/stores/purchaseSummary.js"
import { useStoreDiagnostic } from "@/stores/diagnostic.js"
import { formatNumber } from "@/utils.js"
import diagnosticsFieldsService from "@/services/diagnosticsFields.js"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

/* Stores */
const route = useRoute()
const storePurchaseSummary = useStorePurchaseSummary()
const storeDiagnostic = useStoreDiagnostic()

/* Fields */
const pageName = route.name
const fields = computed(() => diagnosticsFieldsService.getPageFields(pageName))

/* Saisie automatique */
const diagYear = storeDiagnostic.diagnosticCurrentCampaign.year
const { purchaseSummary } = storeToRefs(storePurchaseSummary)
const hasPurchaseSummary = computed(() => storePurchaseSummary.hasPurchaseTotal(diagYear))
</script>
<template>
  <div class="fr-grid-row fr-grid-row--gutters fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Choisissez votre mode de saisie</h2>
      <p>Deux formats existent pour les modes de saisie des données d’approvisionnements EGalim. Un troisième est disponible si vous utilisez l'Outil de Suivi des Achats <em>ma cantine</em>.</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Télédéclaration simplifiée ou détaillée : laquelle choisir ?">
        <a target="_blank" :href="documentation.teledeclarationType">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <div class="gestionnaire-tunnel-mode-saisie__columns">
    <ul class="ma-cantine--unstyled-list fr-grid-row fr-grid-row--gutters">
      <li class="fr-col-12 fr-col-md-4">
        <DsfrBadge
          :no-icon="true"
          label="Saisie simplifiée"
          type="info"
          class="fr-mb-1w fr-mt-2w"
        />
        <p>
          Vous ne distinguez pas vos achats par famille de produit (sauf Viandes et volailles) et vous regroupez les labels par groupes de catégories EGalim (Bio, SIQO, Autres, etc.).
        </p>
        <p>Montants d'achats totaux toutes familles confondues + zoom sur les familles «&nbsp;Viandes Volailles&nbsp;» et «&nbsp;Produits de la mer et aquaculture&nbsp;».</p>
        <p class="fr-hint-text">11 champs dont 6 obligatoires</p>
      </li>
      <li class="fr-col-12 fr-col-md-4">
        <DsfrBadge
          :no-icon="true"
          label="Saisie détaillée"
          type="info"
          class="fr-mb-1w fr-mt-2w"
        />
        <p>Vous fonctionnez avec un suivi segmenté de vos achats par familles (8 familles) en suivant précisément chaque catégorie EGalim (Bio, Label Roug, IGP, Commerce équitable, etc.).</p>
        <p>Compléter les montants totaux par familles de produits pour chacune des catégorie EGalim.</p>
        <p class="fr-hint-text">100 champs, dont 75 obligatoires</p>
      </li>
      <li class="fr-col-12 fr-col-md-4">
        <DsfrBadge
          :no-icon="true"
          label="Saisie automatique"
          type="info"
          class="fr-mb-1w fr-mt-2w"
        />
        <div v-if="hasPurchaseSummary">
          <p>Vous utilisez l'Outil de Suivi des Achats <em>ma cantine</em>.</p>
          <p><span class="fr-text--bold">{{ formatNumber(purchaseSummary[diagYear].valeurTotale) }}€</span> d’achats détectés dans <AppLinkRouter :to="{ name: 'PurchasesHome' }" title="votre suivi des achats" target="_blank"/>.</p>
        </div>
        <p v-else>Vous n'utilisez pas l'Outil de Suivi des Achats <em>ma cantine</em>.</p>
      </li>
    </ul>
    <TunnelTeledeclarationField v-for="field in fields" :key="field" :name="field" class="gestionnaire-tunnel-mode-saisie__fields-container" :class="{ 'hide-auto': !hasPurchaseSummary }" />
  </div>
</template>

<style lang="scss">
.gestionnaire-tunnel-mode-saisie {

  // Customs style to add some borders between columns text and radio
  &__columns {
    overflow: hidden;
    li:nth-child(1), li:nth-child(2) {
      position: relative;
      &::after {
        content: "";
        position: absolute;
        top: 0;
        width: 1px;
        height: 100vw;
        background-color: var(--border-default-grey);
      }
    }

    li:nth-child(2) {
      &::after {
        right: 0px;
      }
    }

    li:nth-child(1) {
      &::after {
        right: -1px;
      }
    }
  }

  &__fields-container {
    .fr-fieldset {
      margin-bottom: 0 !important;
    }

    .fr-fieldset__element {
      max-width: 33.33333% !important;
      margin-bottom: 0 !important;
    }

    &.hide-auto {
      .fr-fieldset__element:last-child {
        display: none !important;
      }
    }
  }
}
</style>
