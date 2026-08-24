<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"
import diagnosticsFieldsService from "@/services/diagnosticsFields"
import documentation from "@/data/documentation.json"
import AppHelpCard from "@/components/AppHelpCard.vue"
import TunnelTeledeclarationField from "@/components/TunnelTeledeclarationField.vue"

const route = useRoute()
const pageName = route.name
const fields = computed(() => diagnosticsFieldsService.getPageFields(pageName))
</script>

<template>
  <div class="fr-grid-row fr-grid-row--gutters">
    <div class="fr-col-12 fr-col-md-7">
      <h2>Estimer mon nombre de couverts annuel</h2>
      <p>Ce chiffre doit refléter la réalité des approvisionnements déclarés sur l’année, en tenant compte des repas complets et des repas partiels (petit-déjeuner, collation…).</p>
    </div>
    <div class="fr-col-12 fr-col-md-5">
      <AppHelpCard title="Bien estimer son nombre de couverts" content="Pour toute question sur le calcul du nombre de couverts : ">
        <a target="_blank" :href="documentation.calculerNombreCouverts">Consultez notre article dédié</a>
      </AppHelpCard>
    </div>
  </div>
  <div class="fr-col-12 fr-col-md-7">
    <TunnelTeledeclarationField v-for="field in fields" :key="field" :name="field" />
  </div>
</template>
