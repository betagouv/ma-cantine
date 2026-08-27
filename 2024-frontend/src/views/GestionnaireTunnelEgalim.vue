<script setup>
import { computed } from "vue"
import { useStoreDiagnostic } from "@/stores/diagnostic"
import { storeToRefs } from "pinia"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

const storeDiagnostic = useStoreDiagnostic()
const { diagnosticCurrentCampaign } = storeToRefs(storeDiagnostic)
const diagIsSimple = computed(() => diagnosticCurrentCampaign.value.diagnosticType === "SIMPLE")
</script>
<template>
  <h2 class="fr-h6">1 - Total des approvisionnements toutes familles de produits confondus :</h2>
  <div class="fr-grid-row fr-grid-row--gutters fr-grid-row--top">
    <div class="fr-col-12 fr-col-md-7">
      <TunnelTeledeclarationField name="valeurTotale" />
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Comment comptabiliser les produits ayant plusieurs labels ?">
        <a :href="documentation.teledeclaration" target="_blank">Je consulte l'aide</a>
      </AppHelpCard>
    </div>
  </div>
  <pre>{{ diagnosticCurrentCampaign }}</pre>
  <pre>{{ diagIsSimple }}</pre>
</template>
