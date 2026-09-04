<script setup>
import { computed } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import { storeToRefs } from "pinia"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"
import DiagnosticEgalimSimple from "@/components/DiagnosticEgalimSimple.vue"

const storeDiagnostic = useStoreDiagnostic()
const { diagnosticCurrentCampaign } = storeToRefs(storeDiagnostic)
const diagIsSimple = computed(() => diagnosticCurrentCampaign.value.diagnosticType === "SIMPLE")
</script>
<template>
  <h2 class="fr-h5">1. Total des approvisionnements toutes familles de produits confondus :</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top fr-mb-4w">
    <div class="fr-col-12 fr-col-md-7">
      <TunnelTeledeclarationField name="valeurTotale" size="full" />
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Comment comptabiliser les produits ayant plusieurs labels ?">
        <a :href="documentation.qualiteDurabiliteProduits" target="_blank">Consultez la documentation</a>
      </AppHelpCard>
    </div>
  </div>
  <DiagnosticEgalimSimple v-if="diagIsSimple" />
</template>
