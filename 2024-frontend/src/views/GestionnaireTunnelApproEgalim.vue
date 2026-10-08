<script setup>
import { computed } from "vue"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { storeToRefs } from "pinia"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import DiagnosticEgalimSimple from "@/components/DiagnosticEgalimSimple.vue"
import DiagnosticEgalimComplete from "@/components/DiagnosticEgalimComplete.vue"
import AppLinkRouter from "@/components/AppLinkRouter.vue"
import teledeclarationFields from "@/data/teledeclaration.json"

/* Fields names */
const valeurTotalFieldName = teledeclarationFields.groups["valeurTotale"][0]
const coutRepasFieldName = teledeclarationFields.groups["coutRepas"][0]

/* Teledeclaration */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic, isSimple, isComplete } = storeToRefs(storeTeledeclaration)

/* Meal count */
const coutRepas = computed(() => diagnostic.value[coutRepasFieldName] || '-')
const updateCoutRepas = async () => await storeTeledeclaration.updateMealCount()
</script>
<template>
  <DsfrAlert
    type="info"
    title="Nouveauté EGalim : la loi UPSA élargit les catégories de produits éligibles depuis le 18 août 2026."
    class="fr-mb-4w"
  >
    <p>
      En phase transitoire, comptabilisez ces produits dans les catégories existantes. De nouvelles catégories seront
      créées pour la télédéclaration 2028. En savoir plus :
      <AppLinkRouter :to="{ name: 'ComprendreMesObligations' }" title="Comprendre mes obligations" />
    </p>
  </DsfrAlert>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Approvisionnements EGalim</h2>
      <p class="fr-mb-0">
        Étape principale et obligatoire de la télédéclaration. Permet de renseigner vos achats au regard des 12
        catégories EGalim. En télédéclaration simplifiée, ces 12 catégories sont regroupées en quatre groupes (bio,
        SIQO, autres EGalim, critères d'achats).
      </p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="En savoir plus sur les 12 catégories EGalim">
        <ul class="ma-cantine--unstyled-list fr-mb-0">
          <li class="fr-mb-1w">
            <a :href="`${documentation.qualiteDurabiliteProduits}/#1-les-12-categories-egalim`" target="_blank">Les 12 catégories</a>
          </li>
          <li class="fr-mb-1w">
            <a :href="documentation.teledeclarationAntiseche" target="_blank">Antisèche</a>
          </li>
          <li class="fr-mb-1w">
            <a :href="documentation.teledeclarationKit" target="_blank">Kit du télédéclarant</a>
          </li>
        </ul>
      </AppHelpCard>
    </div>
  </div>
  <h2 class="fr-h5">1. Total des approvisionnements toutes familles de produits confondus :</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <TunnelTeledeclarationField :name="valeurTotalFieldName" size="full" @change="updateCoutRepas" />
      <DsfrCallout>
        Estimation du coût moyen par repas servi : <span class="fr-text--bold">{{ coutRepas }} €</span>
      </DsfrCallout>
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
