<script setup>
import { computed } from "vue"
import { useStoreTeledeclaration } from "@/stores/teledeclaration"
import { storeToRefs } from "pinia"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import DiagnosticEgalimSimple from "@/components/DiagnosticEgalimSimple.vue"
import DiagnosticEgalimComplete from "@/components/DiagnosticEgalimComplete.vue"
import teledeclarationFields from "@/data/teledeclaration.json"

/* Fields names */
const valeurTotalFieldName = teledeclarationFields.groups["valeurTotale"][0]
const coutRepasFieldName = teledeclarationFields.groups["coutRepas"][0]

/* Teledeclaration */
const storeTeledeclaration = useStoreTeledeclaration()
const { diagnostic } = storeToRefs(storeTeledeclaration)
const diagIsSimple = computed(() => diagnostic.value.diagnosticType === "SIMPLE")

/* Meal count */
const coutRepas = computed(() => diagnostic.value[coutRepasFieldName] || '-')
const updateCoutRepas = async () => await storeTeledeclaration.updateMealCount()
</script>
<template>
  <h2 class="fr-h5">1. Total des approvisionnements toutes familles de produits confondus :</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <TunnelTeledeclarationField :name="valeurTotalFieldName" size="full" @change="updateCoutRepas" />
      <DsfrCallout>
        Estimation du coût moyen par repas servi : <span class="fr-text--bold">{{ coutRepas }} €</span>
      </DsfrCallout>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Comment comptabiliser les produits ayant plusieurs labels ?">
        <a :href="documentation.qualiteDurabiliteProduits" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <DiagnosticEgalimSimple v-if="diagIsSimple" />
  <DiagnosticEgalimComplete v-else />
</template>
